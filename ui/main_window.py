"""Main window with toolbar, results table, log panel, and status bar."""

import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem, QTextBrowser, QFileDialog,
    QStatusBar, QSplitter, QFrame, QHeaderView, QAbstractItemView,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QFont, QIcon

from core.worker import ProcessorWorker
from core.logger import AppLogger
from core.processor import COLUMN_MAP
from ui.theme import dark_theme, light_theme


APP_VERSION = "1.0.0"


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self._zip_path = ""
        self._col_index = 1  # Default column: value_a
        self._dark_mode = True
        self._worker = None
        self._row_counter = 0
        self._logger = AppLogger()

        self._init_ui()
        self._apply_theme()
        self._update_column_button()

    def _init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("PythonStd \u2014 CSV Std Calculator")
        self.setMinimumSize(900, 650)
        self.resize(960, 700)

        # Central widget
        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(16, 16, 16, 8)
        main_layout.setSpacing(12)

        # ===== TOP: Toolbar =====
        toolbar_frame = QFrame()
        toolbar_frame.setObjectName("toolbarFrame")
        toolbar_layout = QHBoxLayout(toolbar_frame)
        toolbar_layout.setContentsMargins(12, 8, 12, 8)
        toolbar_layout.setSpacing(10)

        # Select ZIP button
        self.btn_select = QPushButton("\U0001F4C1  Select ZIP File")
        self.btn_select.setToolTip("Open a ZIP archive containing CSV files")
        self.btn_select.setCursor(Qt.PointingHandCursor)
        self.btn_select.clicked.connect(self._on_select_zip)
        toolbar_layout.addWidget(self.btn_select)

        # Path label
        self.lbl_path = QLabel("No file selected")
        self.lbl_path.setObjectName("pathLabel")
        self.lbl_path.setMinimumWidth(150)
        toolbar_layout.addWidget(self.lbl_path, stretch=1)

        # Mode switch button
        self.btn_mode = QPushButton("\U0001F504  Col: value_a")
        self.btn_mode.setToolTip("Switch processing column (value_a / value_b / value_c)")
        self.btn_mode.setCursor(Qt.PointingHandCursor)
        self.btn_mode.clicked.connect(self._on_mode_switch)
        toolbar_layout.addWidget(self.btn_mode)

        # Theme toggle button
        self.btn_theme = QPushButton("\U0001F319  Dark")
        self.btn_theme.setToolTip("Toggle dark/light theme")
        self.btn_theme.setCursor(Qt.PointingHandCursor)
        self.btn_theme.clicked.connect(self._on_theme_toggle)
        toolbar_layout.addWidget(self.btn_theme)

        # Run / Stop button
        self.btn_run = QPushButton("\u25B6  RUN")
        self.btn_run.setObjectName("btnRun")
        self.btn_run.setToolTip("Start processing CSV files")
        self.btn_run.setCursor(Qt.PointingHandCursor)
        self.btn_run.clicked.connect(self._on_run)
        toolbar_layout.addWidget(self.btn_run)

        main_layout.addWidget(toolbar_frame)

        # ===== MIDDLE + BOTTOM: Splitter =====
        splitter = QSplitter(Qt.Vertical)
        splitter.setHandleWidth(4)

        # Results table
        table_container = QWidget()
        table_vbox = QVBoxLayout(table_container)
        table_vbox.setContentsMargins(0, 0, 0, 0)
        table_vbox.setSpacing(4)

        lbl_results = QLabel("\u2726  Results")
        lbl_results.setObjectName("sectionLabel")
        table_vbox.addWidget(lbl_results)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["#", "Filename", "Standard Deviation (Std)", "Status"])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)

        # Column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(2, 220)
        self.table.setColumnWidth(3, 80)

        table_vbox.addWidget(self.table)
        splitter.addWidget(table_container)

        # Log panel
        log_container = QWidget()
        log_vbox = QVBoxLayout(log_container)
        log_vbox.setContentsMargins(0, 0, 0, 0)
        log_vbox.setSpacing(4)

        lbl_log = QLabel("\u2630  Log")
        lbl_log.setObjectName("sectionLabel")
        log_vbox.addWidget(lbl_log)

        self.log_browser = QTextBrowser()
        self.log_browser.setOpenExternalLinks(False)
        self.log_browser.setMinimumHeight(100)
        log_vbox.addWidget(self.log_browser)
        splitter.addWidget(log_container)

        # Splitter proportions: 65% table, 35% log
        splitter.setSizes([400, 220])
        main_layout.addWidget(splitter, stretch=1)

        # ===== BOTTOM BAR: Status bar =====
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(f"PythonStd v{APP_VERSION}  |  Ready")

    # ---- Theme ----

    def _apply_theme(self):
        """Apply the current theme stylesheet."""
        qss = dark_theme() if self._dark_mode else light_theme()
        self.setStyleSheet(qss)
        self._apply_titlebar_theme(self._dark_mode)

    def _apply_titlebar_theme(self, dark: bool):
        """Apply dark mode to native Windows window title bar."""
        import sys
        if sys.platform == "win32":
            import ctypes
            try:
                # DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                hwnd = int(self.winId())
                value = ctypes.c_int(1 if dark else 0)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    20,
                    ctypes.byref(value),
                    ctypes.sizeof(value)
                )
            except Exception:
                pass

    def _on_theme_toggle(self):
        """Toggle between dark and light themes."""
        self._dark_mode = not self._dark_mode
        self._apply_theme()
        if self._dark_mode:
            self.btn_theme.setText("\U0001F319  Dark")
        else:
            self.btn_theme.setText("\u2600  Light")
        self._log_info(f"Theme switched to {'Dark' if self._dark_mode else 'Light'} mode")

    # ---- File Selection ----

    def _on_select_zip(self):
        """Open file dialog to select a ZIP file."""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select ZIP Archive",
            "",
            "ZIP Archives (*.zip);;All Files (*)",
        )
        if path:
            self._zip_path = path
            basename = os.path.basename(path)
            self.lbl_path.setText(f"\U0001F4CE {basename}")
            self.lbl_path.setToolTip(path)
            self._log_info(f"Selected file: <b>{basename}</b>")
            self.status_bar.showMessage(f"PythonStd v{APP_VERSION}  |  File: {basename}")

    # ---- Column Mode ----

    def _update_column_button(self):
        """Update the mode button text to reflect current column."""
        col_name = COLUMN_MAP.get(self._col_index, "value_a")
        self.btn_mode.setText(f"\U0001F504  Col: {col_name}")

    def _on_mode_switch(self):
        """Cycle through columns 1 -> 2 -> 3 -> 1."""
        self._col_index = (self._col_index % 3) + 1
        self._update_column_button()
        col_name = COLUMN_MAP.get(self._col_index, "value_a")
        self._log_info(f"Switched to column: <b>{col_name}</b> (index {self._col_index})")

    # ---- Run / Stop ----

    def _on_run(self):
        """Start or stop processing."""
        if self._worker is not None and self._worker.isRunning():
            # Stop
            self._worker.stop()
            self.btn_run.setText("\u25B6  RUN")
            self.btn_run.setObjectName("btnRun")
            self._apply_theme()
            self._log_warning("Stopping...")
            return

        if not self._zip_path:
            self._log_error("No ZIP file selected! Click 'Select ZIP File' first.")
            return

        if not os.path.isfile(self._zip_path):
            self._log_error(f"File not found: {self._zip_path}")
            return

        # Clear previous results
        self.table.setRowCount(0)
        self._row_counter = 0
        self.log_browser.clear()
        self._logger.clear()

        # Switch button to STOP mode
        self.btn_run.setText("\u23F9  STOP")
        self.btn_run.setObjectName("btnStop")
        self._apply_theme()

        # Disable other buttons during processing
        self.btn_select.setEnabled(False)
        self.btn_mode.setEnabled(False)

        # Create and start worker
        self._worker = ProcessorWorker(self._zip_path, self._col_index)
        self._worker.progress.connect(self._on_worker_progress)
        self._worker.result.connect(self._on_worker_result)
        self._worker.file_error.connect(self._on_worker_file_error)
        self._worker.file_started.connect(self._on_worker_file_started)
        self._worker.finished_all.connect(self._on_worker_finished)
        self._worker.error.connect(self._on_worker_critical_error)
        self._worker.stats.connect(self._on_worker_stats)
        self._worker.start()

    def _on_worker_progress(self, html_msg: str):
        """Append a progress message to the log."""
        self.log_browser.append(html_msg)
        # Auto-scroll
        sb = self.log_browser.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _on_worker_file_started(self, filename: str):
        """Add a placeholder row for a file that started processing."""
        row = self.table.rowCount()
        self.table.insertRow(row)
        self._row_counter += 1

        # # column
        item_num = QTableWidgetItem(str(self._row_counter))
        item_num.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 0, item_num)

        # Filename
        item_name = QTableWidgetItem(filename)
        self.table.setItem(row, 1, item_name)

        # Std placeholder
        item_std = QTableWidgetItem("...")
        item_std.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 2, item_std)

        # Status: processing
        item_status = QTableWidgetItem("\u23F3")
        item_status.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 3, item_status)

        self.table.scrollToBottom()

    def _on_worker_result(self, filename: str, std_val: float):
        """Update the table row with a successful result."""
        row = self._find_row_by_filename(filename)
        if row < 0:
            return

        # Update Std column
        item_std = QTableWidgetItem(f"{std_val:.6f}")
        item_std.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 2, item_std)

        # Update Status column
        item_status = QTableWidgetItem("\u2714")
        item_status.setTextAlignment(Qt.AlignCenter)
        item_status.setForeground(QColor("#c3e88d"))
        self.table.setItem(row, 3, item_status)

    def _on_worker_file_error(self, filename: str, error_msg: str):
        """Update the table row with an error."""
        row = self._find_row_by_filename(filename)
        if row < 0:
            return

        # Update Std column with error
        item_std = QTableWidgetItem(error_msg)
        item_std.setTextAlignment(Qt.AlignCenter)
        item_std.setForeground(QColor("#f07178"))
        self.table.setItem(row, 2, item_std)

        # Update Status
        item_status = QTableWidgetItem("\u2716")
        item_status.setTextAlignment(Qt.AlignCenter)
        item_status.setForeground(QColor("#f07178"))
        self.table.setItem(row, 3, item_status)

    def _on_worker_stats(self, ok_count: int, err_count: int, elapsed: float):
        """Update the status bar with final stats."""
        self.status_bar.showMessage(
            f"PythonStd v{APP_VERSION}  |  "
            f"Done: {ok_count} OK, {err_count} errors  |  "
            f"Time: {elapsed:.2f}s"
        )

    def _on_worker_finished(self):
        """Called when the worker finishes all processing."""
        self.btn_run.setText("\u25B6  RUN")
        self.btn_run.setObjectName("btnRun")
        self._apply_theme()

        self.btn_select.setEnabled(True)
        self.btn_mode.setEnabled(True)
        self._worker = None

    def _on_worker_critical_error(self, error_msg: str):
        """Handle a critical error from the worker."""
        self._log_error(error_msg)
        self._on_worker_finished()

    def _find_row_by_filename(self, filename: str) -> int:
        """Find a table row by filename. Returns -1 if not found."""
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)
            if item and item.text() == filename:
                return row
        return -1

    # ---- Logging Helpers ----

    def _log_info(self, msg: str):
        html = self._logger.info(msg)
        self.log_browser.append(html)
        sb = self.log_browser.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _log_success(self, msg: str):
        html = self._logger.success(msg)
        self.log_browser.append(html)
        sb = self.log_browser.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _log_warning(self, msg: str):
        html = self._logger.warning(msg)
        self.log_browser.append(html)
        sb = self.log_browser.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _log_error(self, msg: str):
        html = self._logger.error(msg)
        self.log_browser.append(html)
        sb = self.log_browser.verticalScrollBar()
        sb.setValue(sb.maximum())

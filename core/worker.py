"""QThread worker for background CSV processing."""

import time
from PySide6.QtCore import QThread, Signal
from core.processor import list_csv_files, process_single_csv, get_column_name


class ProcessorWorker(QThread):
    """Worker thread that processes CSV files from a ZIP archive."""

    # Signals
    progress = Signal(str)          # HTML-formatted log message
    result = Signal(str, float)     # (filename, std_value) for successful results
    file_error = Signal(str, str)   # (filename, error_message) for failed files
    finished_all = Signal()         # Emitted when all files are processed
    error = Signal(str)             # Critical error (can't open ZIP, etc.)
    file_started = Signal(str)      # Emitted when a file starts processing
    stats = Signal(int, int, float) # (total_ok, total_err, elapsed_seconds)

    def __init__(self, zip_path: str, col_index: int = 1, parent=None):
        super().__init__(parent)
        self._zip_path = zip_path
        self._col_index = col_index
        self._stopped = False

    def stop(self):
        """Request the worker to stop processing."""
        self._stopped = True

    def run(self):
        """Main processing loop."""
        start_time = time.time()
        col_name = get_column_name(self._col_index)

        self.progress.emit(
            f'<span style="color:#82aaff;">\u2139 INFO</span> '
            f'Starting processing with column: <b>{col_name}</b> (index {self._col_index})'
        )

        # List CSV files
        try:
            csv_files = list_csv_files(self._zip_path)
        except RuntimeError as e:
            self.error.emit(str(e))
            return

        if not csv_files:
            self.error.emit("No CSV files found in the ZIP archive.")
            return

        total = len(csv_files)
        self.progress.emit(
            f'<span style="color:#82aaff;">\u2139 INFO</span> '
            f'Found <b>{total}</b> CSV file(s) in archive'
        )

        ok_count = 0
        err_count = 0

        for i, csv_name in enumerate(csv_files, 1):
            if self._stopped:
                self.progress.emit(
                    f'<span style="color:#ffcb6b;">\u26a0 WARNING</span> '
                    f'Processing cancelled by user at file {i}/{total}'
                )
                break

            self.file_started.emit(csv_name)
            self.progress.emit(
                f'<span style="color:#82aaff;">\u2139 INFO</span> '
                f'[{i}/{total}] Processing: <b>{csv_name}</b>'
            )

            filename, std_val, err_msg = process_single_csv(
                self._zip_path, csv_name, self._col_index
            )

            if err_msg is not None:
                err_count += 1
                self.file_error.emit(filename, err_msg)
                self.progress.emit(
                    f'<span style="color:#f07178;">\u2716 ERROR</span> '
                    f'{filename}: {err_msg}'
                )
            else:
                ok_count += 1
                self.result.emit(filename, std_val)
                self.progress.emit(
                    f'<span style="color:#c3e88d;">\u2714 SUCCESS</span> '
                    f'{filename}: std = <b>{std_val:.6f}</b>'
                )

        elapsed = time.time() - start_time
        self.stats.emit(ok_count, err_count, elapsed)
        self.progress.emit(
            f'<span style="color:#c3e88d;">\u2714 SUCCESS</span> '
            f'Completed in <b>{elapsed:.2f}s</b> -- '
            f'{ok_count} succeeded, {err_count} failed'
        )
        self.finished_all.emit()

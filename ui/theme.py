"""Dark and Light QSS themes for the application."""


def dark_theme() -> str:
    """Return the dark theme QSS stylesheet."""
    return """
    /* ===== Global ===== */
    QMainWindow, #centralWidget {
        background-color: #1a1b2e;
    }

    QWidget {
        color: #e0e0e0;
        font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
        font-size: 13px;
    }

    /* ===== Toolbar Frame ===== */
    #toolbarFrame {
        background-color: #252640;
        border: 1px solid #353660;
        border-radius: 10px;
        padding: 8px;
    }

    /* ===== Push Buttons ===== */
    QPushButton {
        background-color: #6c63ff;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 9px 20px;
        font-weight: bold;
        font-size: 13px;
        min-height: 20px;
    }
    QPushButton:hover {
        background-color: #7b73ff;
        border: 1px solid rgba(108, 99, 255, 0.5);
    }
    QPushButton:pressed {
        background-color: #5a52e0;
    }
    QPushButton:disabled {
        background-color: #3a3b55;
        color: #666;
    }

    QPushButton#btnRun {
        background-color: #c3e88d;
        color: #1a1b2e;
        min-width: 100px;
        font-size: 14px;
    }
    QPushButton#btnRun:hover {
        background-color: #d4f5a0;
        border: 1px solid rgba(195, 232, 141, 0.5);
    }

    QPushButton#btnStop {
        background-color: #f07178;
        color: #ffffff;
        min-width: 100px;
        font-size: 14px;
    }
    QPushButton#btnStop:hover {
        background-color: #ff8a90;
        border: 1px solid rgba(240, 113, 120, 0.5);
    }

    /* ===== Table ===== */
    QTableWidget {
        background-color: #1e1f36;
        alternate-background-color: #282a48;
        border: 1px solid #353660;
        border-radius: 8px;
        gridline-color: #353660;
        selection-background-color: rgba(108, 99, 255, 0.3);
        selection-color: #e0e0e0;
        font-size: 13px;
    }
    QTableWidget::item {
        padding: 6px 10px;
        border: none;
    }
    QHeaderView::section {
        background-color: #6c63ff;
        color: #ffffff;
        font-weight: bold;
        padding: 8px 10px;
        border: none;
        font-size: 13px;
    }
    QHeaderView::section:first {
        border-top-left-radius: 8px;
    }
    QHeaderView::section:last {
        border-top-right-radius: 8px;
    }

    /* ===== ScrollBar ===== */
    QScrollBar:vertical {
        background: #1e1f36;
        width: 10px;
        margin: 0;
        border-radius: 5px;
    }
    QScrollBar::handle:vertical {
        background: #6c63ff;
        min-height: 30px;
        border-radius: 5px;
    }
    QScrollBar::handle:vertical:hover {
        background: #7b73ff;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0;
    }
    QScrollBar:horizontal {
        background: #1e1f36;
        height: 10px;
        margin: 0;
        border-radius: 5px;
    }
    QScrollBar::handle:horizontal {
        background: #6c63ff;
        min-width: 30px;
        border-radius: 5px;
    }

    /* ===== Text Browser (Log Panel) ===== */
    QTextBrowser {
        background-color: #0f1020;
        border: 1px solid #353660;
        border-radius: 8px;
        padding: 8px;
        font-family: "Cascadia Code", "Consolas", monospace;
        font-size: 12px;
        color: #c0c0c0;
    }

    /* ===== Status Bar ===== */
    QStatusBar {
        background-color: #252640;
        color: #888;
        border-top: 1px solid #353660;
        font-size: 12px;
        padding: 2px 8px;
    }

    /* ===== Labels ===== */
    QLabel#pathLabel {
        color: #aaa;
        font-size: 12px;
        padding: 0 8px;
    }
    QLabel#sectionLabel {
        color: #6c63ff;
        font-weight: bold;
        font-size: 14px;
        padding: 4px 0;
    }

    /* ===== Splitter ===== */
    QSplitter::handle {
        background-color: #353660;
        height: 2px;
    }
    QSplitter::handle:hover {
        background-color: #6c63ff;
    }

    /* ===== ToolTip ===== */
    QToolTip {
        background-color: #252640;
        color: #e0e0e0;
        border: 1px solid #6c63ff;
        border-radius: 4px;
        padding: 4px 8px;
        font-size: 12px;
    }
    """


def light_theme() -> str:
    """Return the light theme QSS stylesheet."""
    return """
    /* ===== Global ===== */
    QMainWindow, #centralWidget {
        background-color: #f0f2f8;
    }

    QWidget {
        color: #2d2d3a;
        font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
        font-size: 13px;
    }

    /* ===== Toolbar Frame ===== */
    #toolbarFrame {
        background-color: #ffffff;
        border: 1px solid #d8dce8;
        border-radius: 10px;
        padding: 8px;
    }

    /* ===== Push Buttons ===== */
    QPushButton {
        background-color: #5b54d6;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 9px 20px;
        font-weight: bold;
        font-size: 13px;
        min-height: 20px;
    }
    QPushButton:hover {
        background-color: #6b63e6;
        border: 1px solid rgba(91, 84, 214, 0.3);
    }
    QPushButton:pressed {
        background-color: #4a44c0;
    }
    QPushButton:disabled {
        background-color: #c8cad5;
        color: #999;
    }

    QPushButton#btnRun {
        background-color: #43a047;
        color: #ffffff;
        min-width: 100px;
        font-size: 14px;
    }
    QPushButton#btnRun:hover {
        background-color: #4caf50;
        border: 1px solid rgba(67, 160, 71, 0.3);
    }

    QPushButton#btnStop {
        background-color: #e53935;
        color: #ffffff;
        min-width: 100px;
        font-size: 14px;
    }
    QPushButton#btnStop:hover {
        background-color: #ef5350;
        border: 1px solid rgba(229, 57, 53, 0.3);
    }

    /* ===== Table ===== */
    QTableWidget {
        background-color: #ffffff;
        alternate-background-color: #f5f6fa;
        border: 1px solid #d8dce8;
        border-radius: 8px;
        gridline-color: #e8eaf0;
        selection-background-color: rgba(91, 84, 214, 0.15);
        selection-color: #2d2d3a;
        font-size: 13px;
    }
    QTableWidget::item {
        padding: 6px 10px;
        border: none;
    }
    QHeaderView::section {
        background-color: #5b54d6;
        color: #ffffff;
        font-weight: bold;
        padding: 8px 10px;
        border: none;
        font-size: 13px;
    }
    QHeaderView::section:first {
        border-top-left-radius: 8px;
    }
    QHeaderView::section:last {
        border-top-right-radius: 8px;
    }

    /* ===== ScrollBar ===== */
    QScrollBar:vertical {
        background: #f0f2f8;
        width: 10px;
        margin: 0;
        border-radius: 5px;
    }
    QScrollBar::handle:vertical {
        background: #5b54d6;
        min-height: 30px;
        border-radius: 5px;
    }
    QScrollBar::handle:vertical:hover {
        background: #6b63e6;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0;
    }
    QScrollBar:horizontal {
        background: #f0f2f8;
        height: 10px;
        margin: 0;
        border-radius: 5px;
    }
    QScrollBar::handle:horizontal {
        background: #5b54d6;
        min-width: 30px;
        border-radius: 5px;
    }

    /* ===== Text Browser (Log Panel) ===== */
    QTextBrowser {
        background-color: #ffffff;
        border: 1px solid #d8dce8;
        border-radius: 8px;
        padding: 8px;
        font-family: "Cascadia Code", "Consolas", monospace;
        font-size: 12px;
        color: #444;
    }

    /* ===== Status Bar ===== */
    QStatusBar {
        background-color: #ffffff;
        color: #888;
        border-top: 1px solid #d8dce8;
        font-size: 12px;
        padding: 2px 8px;
    }

    /* ===== Labels ===== */
    QLabel#pathLabel {
        color: #777;
        font-size: 12px;
        padding: 0 8px;
    }
    QLabel#sectionLabel {
        color: #5b54d6;
        font-weight: bold;
        font-size: 14px;
        padding: 4px 0;
    }

    /* ===== Splitter ===== */
    QSplitter::handle {
        background-color: #d8dce8;
        height: 2px;
    }
    QSplitter::handle:hover {
        background-color: #5b54d6;
    }

    /* ===== ToolTip ===== */
    QToolTip {
        background-color: #ffffff;
        color: #2d2d3a;
        border: 1px solid #5b54d6;
        border-radius: 4px;
        padding: 4px 8px;
        font-size: 12px;
    }
    """

"""Custom logger with rich HTML formatting for QTextBrowser display."""

from datetime import datetime


# Log level definitions with icons and colors
LOG_LEVELS = {
    "INFO":    {"icon": "\u2139",  "color": "#82aaff"},  # i symbol, blue
    "SUCCESS": {"icon": "\u2714",  "color": "#c3e88d"},  # checkmark, green
    "WARNING": {"icon": "\u26a0",  "color": "#ffcb6b"},  # warning, amber
    "ERROR":   {"icon": "\u2716",  "color": "#f07178"},  # x mark, red
}


class AppLogger:
    """Logger that produces rich HTML messages for display in a QTextBrowser."""

    def __init__(self):
        self._messages = []

    def _format(self, level: str, message: str) -> str:
        """Format a log message as an HTML string."""
        now = datetime.now().strftime("%H:%M:%S")
        cfg = LOG_LEVELS.get(level, LOG_LEVELS["INFO"])
        icon = cfg["icon"]
        color = cfg["color"]

        html = (
            f'<div style="margin:2px 0; font-family: Consolas, monospace; font-size:13px;">'
            f'<span style="color:#888;">[{now}]</span> '
            f'<span style="color:{color}; font-weight:bold;">{icon} {level}</span> '
            f'<span style="color:{color};">{message}</span>'
            f'</div>'
        )
        self._messages.append(html)
        return html

    def info(self, message: str) -> str:
        return self._format("INFO", message)

    def success(self, message: str) -> str:
        return self._format("SUCCESS", message)

    def warning(self, message: str) -> str:
        return self._format("WARNING", message)

    def error(self, message: str) -> str:
        return self._format("ERROR", message)

    def clear(self):
        self._messages.clear()

    @property
    def messages(self):
        return list(self._messages)

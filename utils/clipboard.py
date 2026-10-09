from PySide6.QtGui import QGuiApplication


def copy_to_clipboard(text: str) -> bool:
    clipboard = QGuiApplication.clipboard()
    if clipboard is None or not text:
        return False
    clipboard.setText(text)
    return True

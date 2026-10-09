STYLESHEET = """
QMainWindow, QWidget#central { background-color: #0b1426; }
QWidget { color: #e6edf7; font-size: 13px; }
QLabel#title { font-size: 30px; font-weight: 700; letter-spacing: 2px; color: #ffffff; }
QLabel#subtitle { font-size: 14px; color: #4ea1ff; }
QLabel#section { font-size: 15px; font-weight: 600; color: #ffffff; }
QLabel#warnings { color: #ffb347; }
QFrame#card { background-color: #0f1b31; border: 1px solid #1d2b45; border-radius: 10px; }
QPlainTextEdit, QLineEdit {
    background-color: #08101f; border: 1px solid #24365a; border-radius: 8px;
    padding: 8px; color: #e6edf7; selection-background-color: #2f6fed;
}
QPlainTextEdit:focus, QLineEdit:focus { border: 1px solid #4ea1ff; }
QPushButton {
    background-color: #13223d; border: 1px solid #24365a; border-radius: 8px;
    padding: 8px 16px; font-weight: 600; color: #ffffff;
}
QPushButton:hover { background-color: #1b3157; }
QPushButton#primary { background-color: #2f6fed; border-color: #2f6fed; }
QPushButton#primary:hover { background-color: #4a83f0; }
QRadioButton { spacing: 6px; }
QTableView {
    background-color: #08101f; alternate-background-color: #0f1b31;
    gridline-color: #1d2b45; border: 1px solid #24365a; border-radius: 8px;
    color: #e6edf7; selection-background-color: #2f6fed;
}
QHeaderView::section {
    background-color: #13223d; color: #ffffff; padding: 6px;
    border: none; border-bottom: 1px solid #24365a; font-weight: 600;
}
QMenuBar, QToolBar, QStatusBar { background-color: #0f1b31; color: #e6edf7; }
QMenuBar::item:selected, QMenu::item:selected { background-color: #1b3157; }
QMenu { background-color: #0f1b31; border: 1px solid #24365a; }
QToolBar { border: none; spacing: 6px; }
QToolButton { color: #e6edf7; padding: 4px 8px; }
QToolButton:hover { background-color: #1b3157; border-radius: 4px; }
QPlainTextEdit#codeOutput { font-family: "DejaVu Sans Mono", Consolas, monospace; font-size: 14px; }
QScrollBar:vertical, QScrollBar:horizontal { background: #08101f; border: none; margin: 0; }
QScrollBar:vertical { width: 10px; }
QScrollBar:horizontal { height: 10px; }
QScrollBar::handle { background: #24365a; border-radius: 5px; min-height: 24px; min-width: 24px; }
QScrollBar::handle:hover { background: #4ea1ff; }
QScrollBar::add-line, QScrollBar::sub-line { width: 0; height: 0; }
QScrollBar::add-page, QScrollBar::sub-page { background: none; }
QTextBrowser { background-color: #08101f; border: 1px solid #24365a; border-radius: 8px; }
"""

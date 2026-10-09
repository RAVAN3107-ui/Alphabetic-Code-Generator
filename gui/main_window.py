from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QButtonGroup,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QRadioButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from core.converter import MODE_CHARACTER, MODE_LABELS, ConversionHistory
from gui.mapping_view import MappingView
from gui.notes_view import NotesDialog
from gui.styles import STYLESHEET
from utils.clipboard import copy_to_clipboard


def _section(text: str) -> QLabel:
    label = QLabel(text)
    label.setObjectName("section")
    return label


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Alphabetic Code Generator")
        self.resize(1280, 820)
        self.setStyleSheet(STYLESHEET)
        self.history = ConversionHistory()

        self._build_actions()
        self._build_menus()
        self._build_ui()
        self.statusBar().showMessage("Ready")

    def _build_actions(self) -> None:
        self.generate_action = QAction("Generate", self)
        self.generate_action.setShortcuts([QKeySequence("Ctrl+Return"), QKeySequence("Ctrl+Enter")])
        self.generate_action.triggered.connect(self.generate)

        self.copy_action = QAction("Copy", self)
        self.copy_action.setShortcut(QKeySequence("Ctrl+Shift+C"))
        self.copy_action.triggered.connect(self.copy_output)

        self.clear_action = QAction("Clear", self)
        self.clear_action.setShortcut(QKeySequence("Ctrl+L"))
        self.clear_action.triggered.connect(self.clear)

        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        self.exit_action.triggered.connect(self.close)

        self.notes_action = QAction("Help && Notes", self)
        self.notes_action.setShortcut(QKeySequence.StandardKey.HelpContents)
        self.notes_action.triggered.connect(self.show_notes)

        self.about_action = QAction("About", self)
        self.about_action.triggered.connect(self.show_about)

    def _build_menus(self) -> None:
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addActions([self.generate_action, self.copy_action, self.clear_action])
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        help_menu = self.menuBar().addMenu("&Help")
        help_menu.addActions([self.notes_action, self.about_action])

        toolbar = self.addToolBar("Main")
        toolbar.setMovable(False)
        toolbar.addActions([self.generate_action, self.copy_action, self.clear_action])

    def _build_ui(self) -> None:
        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)

        title = QLabel("ALPHABETIC CODE GENERATOR")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle = QLabel("Convert Text Into Custom Alphabetic Code")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self._build_left_panel())
        self.mapping_view = MappingView()
        splitter.addWidget(self.mapping_view)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)
        splitter.setSizes([780, 460])

        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(8)
        layout.addWidget(splitter, 1)

    def _build_left_panel(self) -> QWidget:
        input_card = QFrame()
        input_card.setObjectName("card")
        self.input_edit = QPlainTextEdit()
        self.input_edit.setPlaceholderText("Type or paste your message here...")

        self.mode_group = QButtonGroup(self)
        modes_grid = QGridLayout()
        for index, (mode, label) in enumerate(MODE_LABELS.items()):
            button = QRadioButton(label)
            button.setProperty("mode", mode)
            button.setChecked(mode == MODE_CHARACTER)
            self.mode_group.addButton(button)
            modes_grid.addWidget(button, index // 3, index % 3)

        generate_button = QPushButton("GENERATE CODE")
        generate_button.setObjectName("primary")
        generate_button.clicked.connect(self.generate)

        mode_row = QHBoxLayout()
        mode_row.addWidget(_section("Conversion Mode"))
        mode_row.addSpacing(12)
        mode_row.addLayout(modes_grid, 1)
        mode_row.addWidget(generate_button, 0, Qt.AlignmentFlag.AlignBottom)

        input_layout = QVBoxLayout(input_card)
        input_layout.addWidget(_section("Enter Your Message"))
        input_layout.addWidget(self.input_edit, 1)
        input_layout.addLayout(mode_row)

        output_card = QFrame()
        output_card.setObjectName("card")
        self.original_edit = QPlainTextEdit()
        self.original_edit.setReadOnly(True)
        self.output_edit = QPlainTextEdit()
        self.output_edit.setReadOnly(True)
        self.output_edit.setObjectName("codeOutput")
        self.warnings_label = QLabel()
        self.warnings_label.setObjectName("warnings")
        self.warnings_label.setWordWrap(True)
        self.warnings_label.hide()

        copy_button = QPushButton("COPY CODE")
        copy_button.clicked.connect(self.copy_output)
        full_button = QPushButton("VIEW FULL")
        full_button.clicked.connect(self.view_full)
        clear_button = QPushButton("CLEAR")
        clear_button.clicked.connect(self.clear)
        buttons = QHBoxLayout()
        for button in (copy_button, full_button, clear_button):
            buttons.addWidget(button)
        buttons.addStretch()

        output_layout = QVBoxLayout(output_card)
        output_layout.addWidget(_section("Original Message"))
        output_layout.addWidget(self.original_edit, 1)
        output_layout.addWidget(_section("Generated Alphabetic Code"))
        output_layout.addWidget(self.output_edit, 2)
        output_layout.addWidget(self.warnings_label)
        output_layout.addLayout(buttons)

        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 8, 0)
        layout.addWidget(input_card, 1)
        layout.addWidget(output_card, 1)
        return panel

    def current_mode(self) -> str:
        return self.mode_group.checkedButton().property("mode")

    def generate(self) -> None:
        text = self.input_edit.toPlainText()
        if not text.strip():
            self.statusBar().showMessage("Enter a message to convert.", 4000)
            return
        mode = self.current_mode()
        result = self.history.convert(text, mode)
        self.original_edit.setPlainText(text)
        self.output_edit.setPlainText(result.output)
        self.warnings_label.setText("\n".join(result.warnings))
        self.warnings_label.setVisible(bool(result.warnings))
        message = f"Converted using {MODE_LABELS[mode]} mode"
        if result.warnings:
            message += f" with {len(result.warnings)} warning(s)"
        self.statusBar().showMessage(message)

    def copy_output(self) -> None:
        if copy_to_clipboard(self.output_edit.toPlainText()):
            self.statusBar().showMessage("Code copied to clipboard.", 4000)
        else:
            self.statusBar().showMessage("Nothing to copy.", 4000)

    def clear(self) -> None:
        for edit in (self.input_edit, self.original_edit, self.output_edit):
            edit.clear()
        self.warnings_label.clear()
        self.warnings_label.hide()
        self.statusBar().showMessage("Cleared.", 4000)

    def view_full(self) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle("Generated Alphabetic Code")
        dialog.resize(720, 480)
        viewer = QPlainTextEdit(self.output_edit.toPlainText())
        viewer.setReadOnly(True)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(dialog.reject)
        layout = QVBoxLayout(dialog)
        layout.addWidget(viewer)
        layout.addWidget(buttons)
        dialog.exec()

    def show_notes(self) -> None:
        NotesDialog(self).exec()

    def show_about(self) -> None:
        QMessageBox.about(
            self,
            "About",
            "Alphabetic Code Generator\n\nConverts text to and from Morse and ROT13 codes.",
        )

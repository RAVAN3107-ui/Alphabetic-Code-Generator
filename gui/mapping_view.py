from PySide6.QtCore import QSortFilterProxyModel, Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QHBoxLayout, QHeaderView, QLabel, QLineEdit, QTableView, QVBoxLayout, QWidget

from mapping.code_mapping import CODE_MAP


class MappingView(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        title = QLabel("Alphabetic Code Mapping")
        title.setObjectName("section")
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText("Filter mapping...")
        self.filter_edit.setClearButtonEnabled(True)

        header = QHBoxLayout()
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.filter_edit)

        self.model = QStandardItemModel(0, 2, self)
        self.model.setHorizontalHeaderLabels(["Character", "Code"])
        for char, code in CODE_MAP.items():
            row = [QStandardItem(char), QStandardItem(code)]
            for item in row:
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setEditable(False)
            self.model.appendRow(row)

        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.proxy.setFilterKeyColumn(-1)
        self.filter_edit.textChanged.connect(self.proxy.setFilterFixedString)

        self.table = QTableView()
        self.table.setModel(self.proxy)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(header)
        layout.addWidget(self.table)

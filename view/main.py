from typing import Optional, Type, List, Dict

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QItemSelection
from PyQt5.QtGui import QColor, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QStackedLayout, QLabel, QDockWidget, QVBoxLayout, \
    QTextEdit, QTreeView, QAbstractItemView

import view
from model import Core
from view.widgets import Title
from view.scene import SectionView


class Application(QApplication):
    app: "Application" = None  # as there should be only one application, I'm creating a singleton
    log_view: Optional["LogView"] = None
    main_window: Optional['MainWindow'] = None

    def __init__(self, core: Core):
        super().__init__([])
        Application.app = self
        self.core: Core = core
        win = Application.main_window = MainWindow()
        win.load_sections()
        self.log("> App Started")

    @classmethod
    def log(cls, text: str):
        if cls.log_view:
            cls.log_view.append(text)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ImagePro 1.0")
        self.setMinimumSize(1000, 700)
        self.setPalette(view.palette_window)
        self.setAutoFillBackground(True)
        self.setFont(view.font)

        self.center_view = CenterView()
        self.setCentralWidget(self.center_view)

        self.algo_tree_view = AlgoTreeView()
        self.algo_tree_view_dock = QDockWidget('Catalog', self)
        self.algo_tree_view_dock.setWidget(self.algo_tree_view)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.algo_tree_view_dock)

        self.image_output_view = ImageOutputView()
        self.image_output_view_dock = QDockWidget("Output", self)
        self.image_output_view_dock.setWidget(self.image_output_view)
        self.addDockWidget(Qt.RightDockWidgetArea, self.image_output_view_dock)

        self.log_view = LogView()
        self.log_view_dock = QDockWidget("Log", self)
        self.log_view_dock.setWidget(self.log_view)
        self.addDockWidget(Qt.RightDockWidgetArea, self.log_view_dock)

        self.show()

    def load_sections(self):
        self.algo_tree_view.load_sections()


class AlgoTreeView(QWidget):
    def __init__(self):
        super().__init__()
        self.sections: List[SectionView] = []
        self.setAutoFillBackground(True)

        lay = QVBoxLayout()
        self.setLayout(lay)

        tree = self.tree = QTreeView()
        lay.addWidget(tree)
        model = QStandardItemModel()
        tree.setModel(model)
        tree.header().setVisible(False)
        tree.selectionModel().selectionChanged.connect(self._selection_changed_slot)
        tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tree.setSelectionMode(QAbstractItemView.SingleSelection)

    def _selection_changed_slot(self, selected: QItemSelection, _: QItemSelection):
        selections = selected.indexes()
        if selections:
            item: QStandardItem = self.tree.model().itemFromIndex(selections[0])
            Application.main_window.center_view.lay.setCurrentWidget(self.sections[item.data(1)])

    def _insert_sections(self, section_item: QStandardItem, section: Type[SectionView]):
        for SubSection in section.subs():
            sub_section_item = QStandardItem(SubSection.name)
            section = SubSection()
            self.sections.append(section)
            Application.main_window.center_view.lay.addWidget(section)
            sub_section_item.setData(len(self.sections)-1, 1)
            section_item.appendRow(sub_section_item)
            self._insert_sections(sub_section_item, SubSection)

    def load_sections(self):
        model = self.tree.model()
        main = model.invisibleRootItem()
        self._insert_sections(main, SectionView)


class CenterView(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        self.lay = QStackedLayout()
        self.setLayout(self.lay)

        lab = Title("CenterView")
        self.lay.addWidget(lab)


class ImageOutputView(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        lay = QVBoxLayout()
        self.setLayout(lay)

        lab = Title("Original Image")
        pal = lab.palette()
        pal.setColor(pal.Background, QColor(255, 0, 0, 64))
        lab.setPalette(pal)
        lab.setAutoFillBackground(True)
        lay.addWidget(lab, 1)

        lab = Title("Accumulator Image")
        pal = lab.palette()
        pal.setColor(pal.Background, QColor(255, 0, 0, 64))
        lab.setPalette(pal)
        lab.setAutoFillBackground(True)
        lay.addWidget(lab, 1)


class LogView(QTextEdit):
    def __init__(self):
        super().__init__()
        Application.log_view = self
        self.setAutoFillBackground(True)
        self.setReadOnly(True)
        self.setMinimumHeight(10)

    def sizeHint(self) -> QtCore.QSize:
        x = super().sizeHint()
        x.setHeight(10)
        return x





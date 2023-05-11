from typing import List, Type

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea

from model import all_subclasses
from view.widgets import Title


class SectionView(QWidget):
    mother: 'SectionView' = None
    name: str = 'Mother'
    order: int = 0

    def __init__(self):
        super().__init__()
        self.subsections: List[Type[SectionView]] = self.subs()

        self._items: List[Type[SectionItem]] = self.items()

        layout = QVBoxLayout()
        self.setLayout(layout)

        lab = Title(f"Section {self.name}")
        lab.setAlignment(Qt.AlignTop)
        lab.setContentsMargins(15, 0, 0, 0)
        layout.addWidget(lab)

        scroll = QScrollArea()
        widget = QWidget()
        lay = QVBoxLayout(widget)
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        for element in self._items:
            lay.addWidget(element())
            lay.addSpacing(10)  # FIXME: the last item shouldn't be added

    @classmethod
    def subs(cls) -> List[Type['SectionView']]:
        ls = [item for item in SectionView.__subclasses__() if item.mother is cls]
        ls.sort(key=lambda e:e.order)
        return ls

    @classmethod
    def items(cls) -> List[Type['SectionItem']]:
        ls = [item for item in all_subclasses(SectionItem) if item.section is cls]
        ls.sort(key=lambda e: e.order)
        return ls


class SectionItem(QWidget):  # must not be subclassed directly
    section: SectionView = None
    order: int = 0

    def __init__(self):
        super().__init__()

        self.lay = QVBoxLayout()
        self.setLayout(self.lay)
        self.lay.addWidget(Title(self.__class__.__name__))


class PlayGround(SectionItem):
    pass


class Description(SectionItem):
    pass


class SectionFilter(SectionView):
    mother = SectionView
    name = 'Filtering'


class DescriptionFilter(Description):
    order = 0
    section = SectionFilter


class PlayGroundFilter(PlayGround):
    order = 1
    section = SectionFilter


class SectionFilterCorrelation(SectionView):
    mother = SectionFilter
    name = 'Correlation'


class SectionFilterCorrelationWindow(SectionView):
    mother = SectionFilterCorrelation
    name = 'Window'


class SectionColors(SectionView):
    mother = SectionView
    name = 'Colors'

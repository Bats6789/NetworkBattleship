from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QStyleOptionGraphicsItem
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QPen
from PyQt6.QtCore import QRectF, Qt
from itertools import product


class BoardView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BoardScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bgImage = QPixmap('QtResources/images/BoardBackground.jpg')

        # Setup game tiles
        sz = self.width() / 11
        coords = product(range(11), range(11))
        self.rects = [Tile(x - 1, y - 1, x == 0 or y == 0, 0, 0, sz, sz) for y, x in coords]

        # Set the properties of the tiles
        for i, rect in enumerate(self.rects):
            if not rect.border:
                rect.setBrush(QColor(49, 149, 202))
                rect.setOpacity(0.8)
            elif i != 0:
                rect.setBrush(QColor(194, 194, 194))
                rect.setOpacity(1)
            else:
                rect.setBrush(QColor(0, 0, 0))
                rect.setOpacity(1)

            rect.setPos((i % 11) * sz, (i // 11) * sz)

            self.addItem(rect)

    def drawBackground(self, painter: QPainter, rect: QRectF):
        winSize = rect.size().toSize()
        painter.drawPixmap(0, 0, winSize.width(), winSize.height(), self.bgImage)


class Tile(QGraphicsRectItem):
    font = QFont('Times', 20, QFont.Weight.Bold)

    def __init__(self, col: int, row: int, isBorder: bool, *args, **kwargs):
        self.row = row
        self.col = col
        self.border = isBorder
        super().__init__(*args, **kwargs)

    def __repr__(self):
        if self.border:
            if self.row == self.col:
                return 'X'
            elif self.col == 9:
                return '10'
            elif self.row == -1:
                return chr(self.col + ord('1'))
            else:
                return chr(self.row + ord('A'))
        else:
            return f'{chr(self.row + ord("A"))}{self.col + 1}'

    def mousePressEvent(self, e):
        print(self)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        super().paint(painter, option, widget)
        if self.border and self.row != self.col:
            painter.setFont(self.font)
            painter.setPen(QPen(QColor(0, 0, 0), 10))
            label = self.__repr__()
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, label)

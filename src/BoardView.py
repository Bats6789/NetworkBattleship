from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QStyleOptionGraphicsItem
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QPen
from PyQt6.QtCore import QRectF, Qt, QEvent, QPointF
from itertools import product


class BoardView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setAcceptHoverEvents(True)

    def hoverMoveEvent(self, e):
        super().hoverMoveEvent(e)
        print('hi')


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

        self.installEventFilter(self)

    def drawBackground(self, painter: QPainter, rect: QRectF):
        winSize = rect.size().toSize()
        painter.drawPixmap(0, 0, winSize.width(), winSize.height(), self.bgImage)

    def getRect(self, point: QPointF):
        for i, rect in enumerate(self.rects):
            x = [rect.pos().x(), rect.pos().x() + rect.rect().width()]
            y = [rect.pos().y(), rect.pos().y() + rect.rect().height()]
            # if rect.contains(point):
            if x[0] <= point.x() <= x[1] and y[0] <= point.y() <= y[1] and not rect.border:
                return i

        return -1

    def eventFilter(self, o, e: QEvent) -> bool:
        if not e:
            return False

        match(e.type()):
            case QEvent.Type.GraphicsSceneMouseMove:
                i = self.getRect(e.scenePos())
                if i != -1:
                    row = i // 11
                    col = i % 11

                    for i, rect in enumerate(self.rects):
                        if not rect.border:
                            if i % 11 == col or i // 11 == row:
                                rect.setBrush(QColor(240, 141, 65))
                            else:
                                rect.setBrush(QColor(49, 149, 202))
                            rect.update()
                self.update()
                return True
            case QEvent.Type.GraphicsSceneLeave:
                for i, rect in enumerate(self.rects):
                    if not rect.border:
                        rect.setBrush(QColor(49, 149, 202))
                        rect.update()
                self.update()
                return True
            case QEvent.Type.GraphicsSceneMousePress:
                self.update()

        return False


class Tile(QGraphicsRectItem):
    font = QFont('Times', 20, QFont.Weight.Bold)

    def __init__(self, col: int, row: int, isBorder: bool, *args, **kwargs):
        self.row = row
        self.col = col
        self.border = isBorder

        super().__init__(*args, **kwargs)

        if not isBorder:
            self.setAcceptHoverEvents(True)

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

    def hoverEnterEvent(self, e):
        if not self.border:
            self.setBrush(QColor(240, 141, 65))
            self.setOpacity(0.8)
        super().hoverEnterEvent(e)

    def hoverLeaveEvent(self, e):
        if not self.border:
            self.setBrush(QColor(49, 149, 202))
            self.setOpacity(0.8)
        super().hoverLeaveEvent(e)

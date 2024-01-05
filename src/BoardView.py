from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtGui import QPixmap, QPainter, QBrush, QImage
from PyQt6.QtCore import Qt


class BoardView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bgImage = QPixmap('QtResources/images/BoardBackground.jpg')

    def paintEvent(self, e):
        print('Paint')
        super().paintEvent(e)
        painter = QPainter(self.bgImage)
        self.scene().drawBackground(painter, e.rect())

        winSize = e.rect().size()
        pixMapRatio = self.bgImage.width() / self.bgImage.height()
        windowRatio = winSize.width() / winSize.height()
        print(winSize)
        print(pixMapRatio, windowRatio)

        if pixMapRatio > windowRatio:
            print('small')
            newWidth = int(winSize.height() * pixMapRatio)
            offset = int((newWidth - winSize.width()) // -2)
            painter.drawPixmap(offset, 0, newWidth, winSize.height(), self.bgImage)
        else:
            print('big')
            newHeight = int(winSize.width() / pixMapRatio)
            painter.drawPixmap(0, 0, winSize.width(), newHeight, self.bgImage)
        pixSize = self.bgImage.size()
        pixSize.scale(winSize, Qt.AspectRatioMode.KeepAspectRatio)
        scaledPix = self.bgImage.scaled(pixSize, Qt.AspectRatioMode.KeepAspectRatio)
        painter.drawPixmap(0, 0, scaledPix)

    # def resizeEvent(self, e):
    #     self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)
    #     print("Resized")


import os
import time

from PyQt5.QtCore import Qt, QRect, QPoint, QThread
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter, QPen, QBrush, QColor, QIcon
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction, \
    qApp, QFileDialog, QWidget, QHBoxLayout
from getLabel import getLayer, getLayeredImg
from StitchImage import stitchImage
from ProgressBar import ProgressBar




#이미지 병합 및 라벨 쓰레드
class Thread(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        #이미지 병합
        self.parent.img, label = stitchImage(self.parent.folderPath)
        #라벨
        self.parent.layerBlock, self.parent.layerRoad, self.parent.layerStruct = getLayer(label)
        self.parent.done = True
        self.stop()

    def stop(self):
        # 멀티쓰레드를 종료하는 메소드
        self.power = False
        self.quit()
        self.wait(3000)

#마우스 클릭 이벤트
class MyLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.begin = QPoint()
        self.end = QPoint()
        self.first = QPoint()
        self.position = []

    def mousePressEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        #shift + 드레그로 사각형 영역 넓이
        if modifiers == Qt.ShiftModifier:
            self.position = []
            imageViewer.pointFlag1=False
            self.first = event.pos()
            self.begin = event.pos()
            self.end = event.pos()
            self.update()
        #두 포인트 클릭으로 거리계산
        else:

            if imageViewer.fitToWindowAct.isChecked():
                w = imageViewer.imageLabel.size().width()
                h = imageViewer.imageLabel.size().height()

                x = event.pos().x() / w * 30000
                y = event.pos().y() / h * 15000
            else:
                x = event.pos().x() / imageViewer.scaleFactor
                y = event.pos().y() / imageViewer.scaleFactor

            x = int(x)
            y = int(y)
            self.update()
            if not imageViewer.pointFlag1:
                self.position = []
                self.point1 = [x, y]
                self.position.append(event.pos())
                imageViewer.mousePosLabel.setText(
                    'Point 1:\nHeight(y): %d\n Width(x):  %d\n\nPoint 2:\nHeight(y): 0.0\n Width(x):  0.0' % (y, x))
                imageViewer.pointFlag1 = True
            elif imageViewer.pointFlag1:
                self.point2 = [x, y]
                self.position.append(event.pos())
                imageViewer.mousePosLabel.setText(
                    'Point 1:\nHeight(y): %d\n Width(x):  %d\n\nPoint 2:\nHeight(y): %d\n Width(x):  %d\n\n distance = %d M' % (
                    self.point1[1], self.point1[0], y, x, self.calDistance()))
                imageViewer.pointFlag1 = False

    def mouseMoveEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier:
            self.end = event.pos()
            self.update()
        else:
            pass

    def mouseReleaseEvent(self, event):

        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier:
            #self.begin = event.pos()
            self.end = event.pos()
            self.update()
            self.calArea()
        else:
            pass

    #
    def paintEvent(self, event):
        super().paintEvent(event)
        modifiers = QApplication.keyboardModifiers()
        #shift + 드레그 사각형 생성
        if modifiers == Qt.ShiftModifier:
            qp = QPainter(self)
            br = QBrush(QColor(255, 10, 10, 40))
            qp.setBrush(br)
            qp.drawRect(QRect(self.begin, self.end))
        #두 포인트 클릭 빨간 점과 두 포인트간 직선 생성
        else:
            qp = QPainter(self)
            qp.setPen(QPen(Qt.red, 8))
            for pos in self.position:
                qp.drawPoint(pos)

            if( len(self.position) == 2):
                qp.setPen(QPen(Qt.red, 4))
                qp.drawLine(self.position[0].x(),self.position[0].y(),self.position[1].x(),self.position[1].y())

    #거리 계산
    def calDistance(self):
        x1 = self.point1[0]
        y1 = self.point1[1]
        x2 = self.point2[0]
        y2 = self.point2[1]
        return int((abs(x2 - x1) ** 2 + abs(y2 - y1) ** 2) ** 0.5 * 0.0647*2)

    #사각형 영역 넓이 계산
    def calArea(self):
        if imageViewer.fitToWindowAct.isChecked():
            w = imageViewer.imageLabel.size().width()
            h = imageViewer.imageLabel.size().height()

            x1 = self.first.x() / w * 30000
            y1 = self.first.y() / h * 15000
            x2 = self.end.x() / w * 30000
            y2 = self.end.y() / h * 15000
        else:
            x1 = self.first.x() / imageViewer.scaleFactor
            y1 = self.first.y() / imageViewer.scaleFactor
            x2 = self.end.x() / imageViewer.scaleFactor
            y2 = self.end.y() / imageViewer.scaleFactor

        imageViewer.mousePosLabel.setText(
            'Point 1:\nHeight(y): %d\n Width(x):  %d\n\nPoint 2:\nHeight(y): %d\n Width(x):  %d\n\nArea = %f M\u00b2' % (
            y1, x1, y2, x2, abs(x2 - x1) * abs(y2 - y1) * 0.0647 * 0.0647*4))

#main window
class QImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scaleFactor = 0.0

        widget = QWidget()

        self.layout = QHBoxLayout(widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(widget)

        self.imageLabel = MyLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)


        self.mousePosLabel = QLabel()
        self.mousePosLabel.setStyleSheet("padding : 30px")


        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setVisible(False)

        # self.setCentralWidget(self.scrollArea)

        self.layout.addWidget(self.scrollArea)
        self.layout.addWidget(self.mousePosLabel)


        self.createActions()
        self.createMenus()
        self.createToolBar()

        self.t1 = Thread(self)

        self.setWindowTitle("Image Viewer")
        self.showMaximized()

    #맵 이미지 표출 및 이미지 있을시에 가능한 도구들 활성화
    def showImage(self):
        self.Qimage = QImage(self.image.data, self.image.shape[1], self.image.shape[0],
                             QImage.Format_RGB888).rgbSwapped()
        self.imageLabel.setPixmap(QPixmap.fromImage(self.Qimage))


        self.scaleFactor = 1.0

        self.scrollArea.setVisible(True)
        self.saveAct.setEnabled(True)
        self.fitToWindowAct.setEnabled(True)
        self.layer1Act.setEnabled(True)
        self.layer2Act.setEnabled(True)
        self.layer3Act.setEnabled(True)
        self.updateActions()
        self.pointFlag1 = False
        self.pointFlag2 = False

        if not self.fitToWindowAct.isChecked():
            self.imageLabel.adjustSize()
            self.scaleImage(0.1)

    #이미지 폴더 선택 및 맵 제작
    def open(self):
        #폴더 선택
        self.folderPath = QFileDialog.getExistingDirectory()
        if self.folderPath:
            self.folderPath = os.path.realpath(self.folderPath)
            self.done = False

            #쓰레드 시작(맵 병합 및 레이어 획득)
            self.t1.start()
            pb = ProgressBar()
            pb.setDescription("Loading")
            while(not self.done):
                time.sleep(0.05)
                QApplication.processEvents()

            pb.close()


            if self.img.size == 0:
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % self.folderPath)
                return

            self.image = self.img
            self.showImage()

    #병합된 원본 이미지 저장
    def save(self):
        fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', '',
                                               "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if fpath:
            self.Qimage.save(fpath)

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def Layer1(self):
        layer1 = self.layer1Act.isChecked()
        layer2 = self.layer2Act.isChecked()
        layer3 = self.layer3Act.isChecked()
        if layer1:
            self.image = getLayeredImg(self.image, self.layerBlock)
            self.showImage()
        if not layer1:
            self.image = self.img
            if layer2:
                self.image = getLayeredImg(self.image, self.layerRoad)
            if layer3:
                self.image = getLayeredImg(self.image, self.layerStruct)
            self.showImage()

    def Layer2(self):
        layer1 = self.layer1Act.isChecked()
        layer2 = self.layer2Act.isChecked()
        layer3 = self.layer3Act.isChecked()
        if layer2:
            self.image = getLayeredImg(self.image, self.layerRoad)
            self.showImage()
        if not layer2:
            self.image = self.img
            if layer1:
                self.image = getLayeredImg(self.image, self.layerBlock)
            if layer3:
                self.image = getLayeredImg(self.image, self.layerStruct)
            self.showImage()

    def Layer3(self):
        layer1 = self.layer1Act.isChecked()
        layer2 = self.layer2Act.isChecked()
        layer3 = self.layer3Act.isChecked()
        if layer3:
            self.image = getLayeredImg(self.image, self.layerStruct)
            self.showImage()
        if not layer3:
            self.image = self.img
            if layer2:
                self.image = getLayeredImg(self.image, self.layerRoad)
            if layer1:
                self.image = getLayeredImg(self.image, self.layerBlock)
            self.showImage()


    def about(self):
        QMessageBox.about(self, "About Image Viewer","...")

    def createActions(self):
        self.openAct = QAction(QIcon(os.path.join(os.path.dirname(__file__), 'ui/open.png')), "&Open...", self, shortcut="Ctrl+O", triggered=self.open)
        self.saveAct = QAction(QIcon(os.path.join(os.path.dirname(__file__),'ui/save.png')), "&Save...", self, shortcut="Ctrl+P", enabled=False, triggered=self.save)
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
        self.zoomInAct = QAction(QIcon(os.path.join(os.path.dirname(__file__),'ui/zoomIn.png')), "Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)
        self.zoomOutAct = QAction(QIcon(os.path.join(os.path.dirname(__file__),'ui/zoomOut.png')), "Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)
        self.normalSizeAct = QAction(QIcon(os.path.join(os.path.dirname(__file__),'ui/normalSize.png')), "&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)
        self.fitToWindowAct = QAction(QIcon(os.path.join(os.path.dirname(__file__),'ui/fitToWindow.png')), "&Fit to Window", self, enabled=False, checkable=True, shortcut="Ctrl+F",
                                      triggered=self.fitToWindow)
        self.layer1Act = QAction(QIcon(os.path.join(os.path.dirname(__file__),'ui/block.png')), "&Show block layer", self, enabled=False, checkable=True, triggered=self.Layer1)
        self.layer2Act = QAction(QIcon(os.path.join(os.path.dirname(__file__),'ui/road.png')), "&Show road layer", self, enabled=False, checkable=True, triggered=self.Layer2)
        self.layer3Act = QAction(QIcon(os.path.join(os.path.dirname(__file__),'ui/structure.png')), "&Show structure layer", self, enabled=False, checkable=True, triggered=self.Layer3)
        self.aboutAct = QAction("&About", self, triggered=self.about)
        self.aboutQtAct = QAction("About &Qt", self, triggered=qApp.aboutQt)

    #상단 도구바
    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.layerMenu = QMenu("&Layer", self)
        self.layerMenu.addAction(self.layer1Act)
        self.layerMenu.addAction(self.layer2Act)
        self.layerMenu.addAction(self.layer3Act)

        self.helpMenu = QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.layerMenu)
        self.menuBar().addMenu(self.helpMenu)

    #상단 툴바
    def createToolBar(self):

        self.statusBar()

        self.toolbar = self.addToolBar('Open')
        self.toolbar.addAction(self.openAct)

        self.toolbar = self.addToolBar('Save')
        self.toolbar.addAction(self.saveAct)


        self.toolbar = self.addToolBar('Zoom In')
        self.toolbar.addAction(self.zoomInAct)

        self.toolbar = self.addToolBar('Zoom Out')
        self.toolbar.addAction(self.zoomOutAct)

        self.toolbar = self.addToolBar('Normal Size')
        self.toolbar.addAction(self.normalSizeAct)

        self.toolbar = self.addToolBar('Fit To Window')
        self.toolbar.addAction(self.fitToWindowAct)

        self.toolbar = self.addToolBar('Block Layer')
        self.toolbar.addAction(self.layer1Act)

        self.toolbar = self.addToolBar('Road Layer')
        self.toolbar.addAction(self.layer2Act)

        self.toolbar = self.addToolBar('Structure Layer')
        self.toolbar.addAction(self.layer3Act)




    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 1.)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.1)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))

    #종료 시 확인창 및 쓰레드 종료
    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # 멀티쓰레드를 종료하는 stop 메소드를 실행함
            self.t1.stop()
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    imageViewer = QImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())


import io
import os.path
from detect import dect
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PIL import Image


class ImageUploader(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Henry\'s LicensePlate')
        self.setGeometry(300, 100, 1280, 800)

        self.leftlayout = QVBoxLayout()
        self.leftlabel = QLabel('等待图片', self)
        image = Image.open("source/load.png")
        pix = self.img2pix(image)
        self.leftlabel.setPixmap(pix)
        self.leftlabel.setFixedSize(640, 640)
        self.leftlayout.addWidget(self.leftlabel)

        self.upload_button = QPushButton('上传图片', self)
        self.upload_button.setFixedSize(640, 160)
        self.upload_button.clicked.connect(self.upload_image)
        self.leftlayout.addWidget(self.upload_button)

        self.rightlayout = QVBoxLayout()
        self.rightlabel = QLabel('等待图片', self)
        image = Image.open("source/wait.png")
        pix = self.img2pix(image)
        self.rightlabel.setPixmap(pix)
        self.rightlabel.setFixedSize(640, 640)
        self.rightlayout.addWidget(self.rightlabel)

        self.dection_button = QPushButton('检测车牌', self)
        self.dection_button.setFixedSize(640, 160)
        self.dection_button.clicked.connect(self.image_dection)
        self.rightlayout.addWidget(self.dection_button)

        self.layout = QHBoxLayout()
        self.layout.addLayout(self.leftlayout)
        self.layout.addLayout(self.rightlayout)
        self.setLayout(self.layout)

    def upload_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
        if file_path:
            self.display_image(file_path)

    def img2pix(self, image):
        byte_array = io.BytesIO()
        image.save(byte_array, format='PNG')
        byte_array.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(byte_array.read())
        return pixmap

    def display_image(self, file_path):
        # 使用PIL加载图像并缩放到720p
        image = Image.open(file_path)
        image.save('source/text.jpg')
        # 使用QPixmap加载和显示图像
        pixmap = self.img2pix(image)
        self.leftlabel.setPixmap(pixmap)
        self.leftlabel.adjustSize()

    def image_dection(self):
        dect("source/text.jpg")
        if os.path.exists("output/labeled_image.jpg"):
            out = self.img2pix(Image.open("output/labeled_image.jpg"))
            self.rightlabel.setPixmap(out)
        else:
            self.rightlabel.setText("没有检测到车牌,\n请检查上传图片")



def main():
    app = QApplication(sys.argv)
    ex = ImageUploader()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

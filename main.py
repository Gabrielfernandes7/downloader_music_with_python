from __future__ import unicode_literals
import os
import sys
import threading
import youtube_dl
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(400, 400, 592, 316)
        self.setWindowTitle("Downloader Music")
        self.font = QtGui.QFont()
        self.font.setFamily("Leelawadee UI")
        self.std_download_path = str(os.path.join(os.path.expanduser("~"), "Downloads"))
        self.initUI()

    def initUI(self):
        self.label_top = QtWidgets.QLabel(self)
        self.label_top.setObjectName("label_top")
        self.label_top.setGeometry(QtCore.QRect(130, 10, 331, 41))
        self.font.setPointSize(22)
        self.font.setBold(True)
        self.font.setWeight(75)
        self.label_top.setFont(self.font)
        self.label_top.setAlignment(QtCore.Qt.AlignCenter)
        self.label_top.setText("Downloader Music")

        self.button_download = QtWidgets.QPushButton(self)
        self.button_download.setObjectName("button_download")
        self.button_download.setGeometry(QtCore.QRect(240, 170, 111, 51))
        self.font.setPointSize(14)
        self.font.setBold(True)
        self.font.setWeight(75)
        self.button_download.setFont(self.font)
        self.button_download.setText("Download")
        self.button_download.clicked.connect(self.download_button)
        
        self.input_url = QtWidgets.QLineEdit(self)
        self.input_url.setObjectName("input_url")
        self.input_url.setGeometry(QtCore.QRect(20, 60, 551, 41))
        self.font.setPointSize(10)
        self.input_url.setFont(self.font)
        self.input_url.setAlignment(QtCore.Qt.AlignCenter)
        self.input_url.setText("")
        self.input_url.setPlaceholderText("Entre com a URL do vídeo aqui ... ")

        self.button_set = QtWidgets.QPushButton(self)
        self.button_set.setObjectName("button_set")
        self.button_set.setGeometry(QtCore.QRect(500, 110, 71, 41))
        self.button_set.setFont(self.font)
        self.button_set.setText("Set")
        self.button_set.clicked.connect(self.set_button)

        self.input_path = QtWidgets.QLineEdit(self)
        self.input_path.setObjectName("input_path")
        self.input_path.setGeometry(QtCore.QRect(20, 110, 471, 41))
        self.input_path.setFont(self.font)
        self.input_path.setAlignment(QtCore.Qt.AlignCenter)
        self.input_path.setText(self.std_download_path)

        self.label_done = QtWidgets.QLabel(self)
        self.label_done.setObjectName("label_done")
        self.label_done.setGeometry(QtCore.QRect(10, 240, 590, 31))
        self.font.setPointSize(14)
        self.font.setBold(False)
        self.font.setWeight(50)
        self.label_done.setFont(self.font)
        self.label_done.setAlignment(QtCore.Qt.AlignCenter)
        self.label_done.setText("")

    def set_button(self):
        file_name = QFileDialog.getExistingDirectory()
        if file_name:
            self.input_path.setText(file_name)

    def download_button(self):
        url = self.input_url.text()
        save_path = self.input_path.text()
        download = threading.Thread(target=self.download_thread, args=(url, save_path), daemon=True)
        download.start()

    def download_thread(self, url, save_path):
        Download(url, save_path).download()
        
        self.input_url.setText("")
        self.label_done.setText("Download Done!")

class Download(object):
    def __init__(self, url, save_path):
        self.url = url
        self.save_path = save_path

    @property
    def song_opts(self):
        return {
            "verbose": False,
            "fixup"  : "detect_or_warn",
            "format" : "bestaudio/best",
            "postprocessors" : [{
                "key": "FFmpegExtractAudio",
                "preferredcodec"  : "mp3",
            }],
            "extractaudio": True,
            "outtmpl"     : self.save_path + "/%(title)s.%(ext)s"
        }
    
    def download(self):
        download_object = youtube_dl.YoutubeDL(self.song_opts)
        info = download_object.extract_info(self.url, download=False)
        song_name = info.get('title', None)
        window.label_done.setText(song_name)
        return download_object.download([self.url])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
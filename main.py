from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLineEdit,
    QApplication,
    QLabel,
    QVBoxLayout,
    QFileDialog,
    QFormLayout,
    QRadioButton,
    QButtonGroup,
    QMessageBox,
    QHBoxLayout,
    QTabWidget,
)
from core.thread import YoutubeDownloadThread, InstagramDownloadThread
import sys
import os

VERSION = "1.0.1-beta"
GITHUB = "https://github.com/JN513"
REPOSITORY = "https://github.com/JN513/youtube_downloader"


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.path_to_save = None
        self.type = 0
        self.ittype = 1
        self.content = 0
        self.basedir = os.path.dirname(os.path.realpath(__file__))

        self.initUI()

    def initUI(self):

        # self.setGeometry(300, 300, 290, 150)

        self.setWindowTitle("Youtube download")

        tabs = QTabWidget()
        tabs.addTab(self.youtube_UI(), "Youtube")
        tabs.addTab(self.instagram_UI(), "Instagram")
        tabs.addTab(self.info_UI(), "Info")

        main_layout = QVBoxLayout()
        main_layout.addWidget(tabs)

        self.setLayout(main_layout)

        self.show()

    def youtube_UI(self):
        youtubeTab = QWidget()

        self.yt_top_label = QLabel()
        self.yt_top_label.setText("Insira um ou mais links separados por ';'.")
        self.yt_input = QLineEdit()

        self.type_label = QLabel()
        self.type_label.setText("Tipo")

        self.rbty1 = QRadioButton("Playlist")
        self.rbty2 = QRadioButton("Video")
        self.rbty2.setChecked(True)

        self.rbty1.toggled.connect(self.onClicked_type)
        self.rbty2.toggled.connect(self.onClicked_type)

        self.content_label = QLabel()
        self.content_label.setText("Conteudo")

        self.rbtn1 = QRadioButton("MP4")
        self.rbtn2 = QRadioButton("MP3")
        self.rbtn2.setChecked(True)

        self.rbtn1.toggled.connect(self.onClicked_content)
        self.rbtn2.toggled.connect(self.onClicked_content)

        self.btngroup1 = QButtonGroup()
        self.btngroup2 = QButtonGroup()

        self.btngroup1.addButton(self.rbtn1)
        self.btngroup1.addButton(self.rbtn2)
        self.btngroup2.addButton(self.rbty1)
        self.btngroup2.addButton(self.rbty2)

        self.label_title_for_label_path = QLabel("Diretorio atual: ")
        self.label_path = QLabel()
        if self.path_to_save == None:
            self.label_path.setText(self.basedir)

        self.label_status = QLabel()
        self.label_status.setText("")

        btn_opendir = QPushButton("Escolher diretorio", self)
        btn_opendir.clicked.connect(self.select_save_dir)

        self.btn_download = QPushButton("Baixar", self)
        self.btn_download.clicked.connect(self.download_yt)

        input_form = QFormLayout()
        input_form.addRow("Links:", self.yt_input)

        layout = QVBoxLayout()
        layout_type = QVBoxLayout()
        layout_content = QVBoxLayout()
        layout_dir = QHBoxLayout()
        layout_status = QHBoxLayout()

        layout.addWidget(btn_opendir)
        layout.addWidget(self.btn_download)

        layout_type.addWidget(self.type_label)
        layout_type.addWidget(self.rbty1)
        layout_type.addWidget(self.rbty2)

        layout_content.addWidget(self.content_label)
        layout_content.addWidget(self.rbtn1)
        layout_content.addWidget(self.rbtn2)

        layout_dir.addWidget(self.label_title_for_label_path)
        layout_dir.addWidget(self.label_path)

        layout_status.addWidget(self.label_status)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.yt_top_label)
        main_layout.addLayout(input_form)
        main_layout.addLayout(layout_type)
        main_layout.addLayout(layout_content)
        main_layout.addLayout(layout_dir)
        main_layout.addLayout(layout_status)
        main_layout.addLayout(layout)

        youtubeTab.setLayout(main_layout)

        return youtubeTab

    def instagram_UI(self):
        instagramTab = QWidget()

        self.it_top_label = QLabel()
        self.it_top_label.setText(
            "Insira um ou mais links ou codigos separados por ';'."
        )
        self.it_input = QLineEdit()

        self.label_title_for_label_path = QLabel("Diretorio atual: ")
        self.label_path = QLabel()
        if self.path_to_save == None:
            self.label_path.setText(self.basedir)

        btn_opendir = QPushButton("Escolher diretorio", self)
        btn_opendir.clicked.connect(self.select_save_dir)

        self.it_btn_download = QPushButton("Baixar", self)
        self.it_btn_download.clicked.connect(self.download_insta)

        self.ittype_label = QLabel("Tipo:")

        self.btngroup3 = QButtonGroup()
        self.itbtn1 = QRadioButton("Link")
        self.itbtn2 = QRadioButton("Codigo")
        self.itbtn2.setChecked(True)

        self.btngroup3.addButton(self.itbtn1)
        self.btngroup3.addButton(self.itbtn2)

        self.itbtn1.toggled.connect(self.onClicked_type)
        self.itbtn2.toggled.connect(self.onClicked_type)

        layout = QVBoxLayout()
        layout_type = QVBoxLayout()
        layout_dir = QHBoxLayout()
        layout_status = QHBoxLayout()

        layout_type.addWidget(self.ittype_label)
        layout_type.addWidget(self.itbtn1)
        layout_type.addWidget(self.itbtn2)

        layout_dir.addWidget(self.label_title_for_label_path)
        layout_dir.addWidget(self.label_path)

        layout.addWidget(btn_opendir)
        layout.addWidget(self.it_btn_download)

        layout_status.addWidget(self.label_status)

        input_form = QFormLayout()
        input_form.addRow("Links:", self.it_input)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.it_top_label)
        main_layout.addLayout(input_form)
        main_layout.addLayout(layout_type)
        main_layout.addLayout(layout_dir)
        main_layout.addLayout(layout_status)
        main_layout.addLayout(layout)

        instagramTab.setLayout(main_layout)

        return instagramTab

    def info_UI(self):
        infoTab = QWidget()

        linkTemplate = "<a href={0}>{1}</a>"

        autor_label = QLabel("Criado por: Julio Nunes Avelar")
        github_label = QLabel("Github: ")
        github_link = QLabel(linkTemplate.format(GITHUB, GITHUB))
        github_link.setOpenExternalLinks(True)
        repositorio_label = QLabel("Repositorio: ")
        repositorio_link = QLabel(linkTemplate.format(REPOSITORY, REPOSITORY))
        repositorio_link.setOpenExternalLinks(True)
        sobre_label = QLabel(
            "Sobre: Este programa foi criado para facilitar o download de vídeos do youtube e instagram."
        )
        version_label = QLabel(f"Versao: {VERSION}")

        github_layout = QHBoxLayout()
        github_layout.addWidget(github_label)
        github_layout.addWidget(github_link)

        repositorio_layout = QHBoxLayout()
        repositorio_layout.addWidget(repositorio_label)
        repositorio_layout.addWidget(repositorio_link)

        main_layout = QVBoxLayout()
        main_layout.addWidget(autor_label)
        main_layout.addLayout(github_layout)
        main_layout.addLayout(repositorio_layout)
        main_layout.addWidget(sobre_label)
        main_layout.addWidget(version_label)

        infoTab.setLayout(main_layout)

        return infoTab

    def select_save_dir(self):
        dir_ = QFileDialog.getExistingDirectory(
            None, "Select a folder:", "~/", QFileDialog.ShowDirsOnly
        )
        self.path_to_save = dir_
        self.label_path.setText(dir_)

    def download_yt(self):

        self.label_status.setText("Fazendo Download ...")
        links = self.yt_input.text()

        if self.path_to_save == None:
            self.path_to_save = self.basedir

        self.thread = QThread()

        self.worker = YoutubeDownloadThread(
            self.path_to_save, links, self.type, self.content
        )

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.thread.deleteLater)
        self.worker.alert.connect(self.alert)

        print(f"Thread criada")

        self.thread.start()

        print(f"Thread iniciada")

        self.btn_download.setEnabled(False)
        self.thread.finished.connect(lambda: self.btn_download.setEnabled(True))
        self.thread.finished.connect(
            lambda: self.label_status.setText("Download(s) Concluidos")
        )

    def download_insta(self):
        self.label_status.setText("Fazendo Download ...")
        links = self.it_input.text()

        if self.path_to_save == None:
            self.path_to_save = self.basedir

        self.thread_it = QThread()

        self.worker_it = InstagramDownloadThread(links, self.path_to_save, self.ittype)

        self.worker_it.moveToThread(self.thread_it)

        self.thread_it.started.connect(self.worker_it.run)
        self.worker_it.finished.connect(self.thread_it.quit)
        self.worker_it.finished.connect(self.thread_it.deleteLater)
        self.worker_it.alert.connect(self.alert)

        print(f"Thread criada")

        self.thread_it.start()

        print(f"Thread iniciada")

        self.it_btn_download.setEnabled(False)
        self.thread_it.finished.connect(lambda: self.it_btn_download.setEnabled(True))
        self.thread_it.finished.connect(
            lambda: self.label_status.setText("Download(s) Concluidos")
        )

    def onClicked_type(self):
        btn = self.sender()
        if btn.isChecked():
            if btn.text() == "Video":
                self.type = 0
            elif btn.text() == "Playlist":
                self.type = 1
            elif btn.text() == "Link":
                self.ittype = 0
            elif btn.text() == "Codigo":
                self.ittype = 1

    def onClicked_content(self):
        btn = self.sender()
        if btn.isChecked():
            if btn.text() == "MP3":
                self.content = 0
            elif btn.text() == "MP4":
                self.content = 1

    def alert(self, content, body):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(content)
        msg.setInformativeText(body)
        msg.setWindowTitle("Info")
        msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

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
)
from moviepy.editor import AudioFileClip
from pytube import YouTube, Playlist
import sys
import os


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.path_to_save = None
        self.type = 0
        self.content = 0
        self.basedir = os.path.dirname(os.path.realpath(__file__))
        self.initUI()

    def initUI(self):

        # self.setGeometry(300, 300, 290, 150)

        self.setWindowTitle("Youtube download")

        self.top_label = QLabel()
        self.top_label.setText("Insira um ou mais links separados por ';'.")
        self.input = QLineEdit()

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

        btn_download = QPushButton("Baixar", self)
        btn_download.clicked.connect(self.download)

        input_form = QFormLayout()
        input_form.addRow("Links:", self.input)

        layout = QVBoxLayout()
        layout_type = QVBoxLayout()
        layout_content = QVBoxLayout()
        layout_dir = QHBoxLayout()
        layout_status = QHBoxLayout()

        layout.addWidget(btn_opendir)
        layout.addWidget(btn_download)

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
        main_layout.addWidget(self.top_label)
        main_layout.addLayout(input_form)
        main_layout.addLayout(layout_type)
        main_layout.addLayout(layout_content)
        main_layout.addLayout(layout_dir)
        main_layout.addLayout(layout_status)
        main_layout.addLayout(layout)

        self.setLayout(main_layout)

        self.show()

    def select_save_dir(self):
        dir_ = QFileDialog.getExistingDirectory(
            None, "Select a folder:", "~/", QFileDialog.ShowDirsOnly
        )
        self.path_to_save = dir_
        self.label_path.setText(dir_)

    def download(self):

        links = self.input.text()
        links = links.split(";")

        if self.path_to_save == None:
            self.path_to_save = self.basedir

        playlist_error = 0
        video_error = 0

        for link in links:
            if self.type == 0:
                try:
                    video = YouTube(link)
                    if self.content == 1:
                        stream = video.streams.get_highest_resolution()
                        self.label_status.setText("Fazendo Download ...")
                        stream.download(self.path_to_save)

                    elif self.content == 0:
                        audio = video.streams.filter(only_audio=True).first()
                        self.label_status.setText("Fazendo Download ...")
                        audio.download(self.path_to_save)
                        self.label_status.setText("Convertendo ...")
                        mp4_path = os.path.join(
                            self.path_to_save, audio.default_filename
                        )
                        mp3_path = os.path.join(
                            self.path_to_save,
                            os.path.splitext(audio.default_filename)[0] + ".mp3",
                        )
                        new_file = AudioFileClip(mp4_path)
                        new_file.write_audiofile(mp3_path)
                        os.remove(mp4_path)
                except:
                    self.alert(
                        "Erro ao baixar video",
                        "Verifique o link e sua conexão com a internet e tente novamente",
                    )
                    video_error += 1
            if self.type == 1:
                try:
                    playlist = Playlist(link)
                    for url in playlist:
                        try:
                            video = YouTube(url)
                            if self.content == 1:
                                stream = video.streams.get_highest_resolution()
                                self.label_status.setText("Fazendo Download ...")
                                stream.download(self.path_to_save)

                            elif self.content == 0:
                                audio = video.streams.filter(only_audio=True).first()
                                self.label_status.setText("Fazendo Download ...")
                                audio.download(self.path_to_save)
                                self.label_status.setText("Convertendo ...")
                                mp4_path = os.path.join(
                                    self.path_to_save, audio.default_filename
                                )
                                mp3_path = os.path.join(
                                    self.path_to_save,
                                    os.path.splitext(audio.default_filename)[0]
                                    + ".mp3",
                                )
                                new_file = AudioFileClip(mp4_path)
                                new_file.write_audiofile(mp3_path)
                                os.remove(mp4_path)
                        except:
                            self.alert(
                                "Erro ao baixar video",
                                "Verifique o link e sua conexão com a internet e tente novamente",
                            )
                            video_error += 1
                except:
                    self.alert(
                        "Erro ao abrir playlist",
                        "Verifique o link e sua conexão com a internet e tente novamente",
                    )
                    playlist_error += 1

        erro = ""
        if playlist_error > 0:
            erro += f" Erro ao abrir {playlist_error} playlists."
        if video_error > 0:
            erro += f" Erro ao baixar {video_error} video(s)."

        self.label_status.setText("Download(s) Concluidos")
        self.alert(
            "Download(s) Concluidos.",
            "Todos os downloads possiveis foram finalizados." + erro,
        )

    def onClicked_type(self):
        btn = self.sender()
        if btn.isChecked():
            if btn.text() == "Video":
                self.type = 0
            elif btn.text() == "Playlist":
                self.type = 1

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

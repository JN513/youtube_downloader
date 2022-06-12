from PyQt5.QtCore import pyqtSignal, QObject
from core.core import download_instagram, download_youtube, download_spotify


class YoutubeDownloadThread(QObject):
    finished = pyqtSignal()
    alert = pyqtSignal(str, str)

    def __init__(self, path_to_save, links, type, content):
        super().__init__()
        self.path_to_save = path_to_save
        self.links = links
        self.type = type
        self.content = content

    def run(self):
        print("YoutubeDownloadThread: run")

        ok, video_error, playlist_error = download_youtube(
            self.links, self.path_to_save, self.type, self.content
        )

        erro = ""
        if playlist_error > 0:
            erro += f" Erro ao abrir {playlist_error} playlists."
        if video_error > 0:
            erro += f" Erro ao baixar {video_error} video(s)."

        self.alert.emit(
            "Download(s) Concluidos.",
            "Todos os downloads possiveis foram finalizados." + erro,
        )

        self.finished.emit()


class InstagramDownloadThread(QObject):
    finished = pyqtSignal()
    alert = pyqtSignal(str, str)

    def __init__(self, links, path_to_save, ittype):
        super().__init__()
        self.links = links
        self.path_to_save = path_to_save
        self.ittype = ittype

    def run(self):
        ok, error = download_instagram(self.links, self.path_to_save, self.ittype)

        erro = ""
        if error > 0:
            erro += f" Erro ao baixar {error} imagem(s)/video(s)."

        self.alert.emit(
            "Download(s) Concluidos.",
            "Todos os downloads possiveis foram finalizados." + erro,
        )

        self.finished.emit()


class SpotifyDownloadThread(QObject):
    finished = pyqtSignal()
    alert = pyqtSignal(str, str)

    def __init__(self, links, path_to_save, format_to_Save = "mp3"):
        super().__init__()
        self.path_to_save = path_to_save
        self.links = links
        self.format_to_Save = format_to_Save

    def run(self):
        ok, error = download_spotify(self.links, self.path_to_save, self.format_to_Save)

        erro = ""
        if error > 0:
            erro += f" Erro ao baixar musica(s)."

        self.alert.emit(
            "Download(s) Concluidos.",
            "Todos os downloads possiveis foram finalizados." + erro,
        )

        self.finished.emit()
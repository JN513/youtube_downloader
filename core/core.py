from moviepy.editor import AudioFileClip
from pytube import YouTube, Playlist
import instaloader
import os
import re


def _download_youtube(url: str, path_to_save: str, content: int):
    try:
        video = YouTube(url)
        if content == 1:
            stream = video.streams.get_highest_resolution()
            stream.download(path_to_save)

        else:
            audio = video.streams.filter(only_audio=True).first()
            audio.download(path_to_save)
            mp4_path = os.path.join(path_to_save, audio.default_filename)
            mp3_path = os.path.join(
                path_to_save,
                os.path.splitext(audio.default_filename)[0] + ".mp3",
            )
            new_file = AudioFileClip(mp4_path)
            new_file.write_audiofile(mp3_path)
            os.remove(mp4_path)

    except Exception as e:
        print(e)
        return False

    return True


def download_youtube(inputs: str, path_to_save: str, type: int, content: int):
    links = inputs.split(";")

    ok = True
    playlist_error = 0
    video_error = 0

    print("Downloading...")

    for link in links:
        if type == 0:
            print("Downloading video...")
            if not _download_youtube(link, path_to_save, content):
                ok = False
                video_error += 1
        if type == 1:
            playlist = Playlist(link)
            print("Downloading playlist...")
            for url in playlist:
                if not _download_youtube(url, path_to_save, content):
                    ok = False
                    playlist_error += 1
                    video_error += 1

    print("Done!")

    return ok, video_error, playlist_error


def download_instagram(inputs: str, path_to_save: str, link_type: int):
    links = inputs.split(";")

    ok = True
    error = 0

    for link in links:
        try:
            found = ""

            if link_type == 0:

                found = re.search(r"https://www.instagram.com/p/([^/]+)/", link)

                if not found:
                    found = re.search(r"https://instagram.com/p/([^/]+)/", link)
                if not found:
                    found = re.search(r"http://www.instagram.com/p/([^/]+)/", link)
                if not found:
                    found = re.search(r"http://instagram.com/p/([^/]+)/", link)
                if not found:
                    found = re.search(r"https://instagram.com/tv/([^/]+)/", link)
                if not found:
                    found = re.search(r"http://www.instagram.com/tv/([^/]+)/", link)
                if not found:
                    found = re.search(r"http://instagram.com/tv/([^/]+)/", link)
                if not found:
                    found = re.search(r"https://www.instagram.com/tv/([^/]+)/", link)
                if not found:
                    ok = False
                    error += 1
                    continue

                found = found.group(1)

            else:
                found = link

            insta = instaloader.Instaloader(
                download_pictures=True,
                download_videos=True,
                download_video_thumbnails=True,
                download_geotags=False,
                download_comments=False,
                save_metadata=False,
                compress_json=False,
                filename_pattern="{profile}_{mediaid}",
            )

            post = instaloader.Post.from_shortcode(insta.context, found)
            insta.download_post(post, path_to_save)

        except Exception as e:
            print(e)
            ok = False
            error += 1

    return ok, error

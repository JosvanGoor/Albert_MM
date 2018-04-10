import threading
import youtube_dl as yt

ydl_opts = {
    'ignoreerrors': True,
    'quiet': False
}

class ytl_worker(threading.Thread):
    def __init__(self, url):
        self.url = url
        threading.Thread.__init__(self)

    def run(self):
        with yt.YoutubeDL(ydl_opts) as ydl:

            playlist_dict = ydl.extract_info(url, download=False)

            for video in playlist_dict['entries']:

                print()

                if not video:
                    print('ERROR: Unable to get info. Continuing...')
                    continue

                print('https://www.youtube.com/watch?v=', video["id"])    
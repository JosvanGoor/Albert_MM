import threading
import youtube_dl as yt

ydl_opts = {
    'ignoreerrors': True,
    'quiet': False
}

class ytl_worker(threading.Thread):
    def __init__(self, url, ytmod):
        self.url = url
        self.ytmod = ytmod
        threading.Thread.__init__(self)

    def run(self):
        with yt.YoutubeDL(ydl_opts) as ydl:
            
            video_links = []

            playlist_dict = ydl.extract_info(self.url, download=False)

            for video in playlist_dict['entries']:

                print()

                if not video:
                    print('ERROR: Unable to get info. Continuing...')
                    continue

                video_links.append('https://www.youtube.com/watch?v=', video["id"]))

        self.ytmod.queue + video_links
        if self.ytmod.state == self.ytmod.STATE_IDLE: # not if were busy tho
            self.ytmod.state = self.ytmod.STATE_STARTING
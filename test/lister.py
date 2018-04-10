import youtube_dl as yt

ydl_opts = {
    'ignoreerrors': True,
    'quiet': False
}

url = 'https://www.youtube.com/watch?v=IsQMpJ5lURQ&list=PL6ABA510E8B9DE95D'

with yt.YoutubeDL(ydl_opts) as ydl:

    playlist_dict = ydl.extract_info(url, download=False)

    for video in playlist_dict['entries']:

        print()

        if not video:
            print('ERROR: Unable to get info. Continuing...')
            continue

        print('https://www.youtube.com/watch?v=', video["id"])

        #for property in ['thumbnail', 'id', 'title', 'description', 'duration', 'url']:
        #    print(property, '--', video.get(property))
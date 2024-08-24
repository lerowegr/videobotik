import youtube_dl

# URL видео на Rutube
video_url = 'https://www.youtube.com/watch?v=Qryn6_ikyh8'

# Опции для youtube_dl
ydl_opts = {
    'listformats': True,  # Эта опция заставляет youtube_dl выводить список форматов
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])
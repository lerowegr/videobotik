import yt_dlp

def download_video_with_quality(youtube_url, output_path='.', video_resolution='1080p', audio_quality='best'):
    print('Эта программа предназначена для загрузки видео с YouTube с возможностью выбора качества видео и аудио. '
          'Вы можете указать желаемое разрешение видео и качество аудио, '
          'чтобы получить оптимальный файл для ваших нужд.')

    try:
        # Запрос разрешения видео и качества аудио у пользователя
        video_resolution = input("Введите желаемое разрешение видео (например, 720p, 1080p, 1440p, 2160p): ").strip()
        audio_quality = input("Введите желаемое качество аудио (low, medium, high, best): ").strip()

        # Формат выбора видео и аудио, чтобы гарантировать mp4 и aac
        video_format = f'bestvideo[ext=mp4][height={video_resolution[:-1]}]'
        audio_format = 'bestaudio[ext=m4a]' if audio_quality == 'best' else f'bestaudio[ext=m4a]/bestaudio'

        # Опции для загрузки
        ydl_opts = {
            'format': f'{video_format}+{audio_format}',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegMerger',
            }],
            'merge_output_format': 'mp4',
            'ffmpeg_location': r"C:\Users\Егор\Documents\GitHub\videobotik\ffmpeg.exe",
        }

        # Скачивание видео
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
            print("Скачивание завершено!")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Пример использования
video_url = 'https://www.youtube.com/watch?v=ehtay-L70RU'
download_video_with_quality(video_url, output_path=r"C:\Users\Егор\Downloads")
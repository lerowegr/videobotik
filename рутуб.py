import youtube_dl

def download_rutube_video(video_url, output_path='.'):
    try:
        ydl_opts = {
            'format': 'm3u8-1014-0',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(video_url, download=True)
            video_title = result.get('title', 'video')
            video_file = f"{output_path}/{video_title}.mp4"
            print("Скачивание завершено!")
            return video_file
    except Exception as e:
        print(f"Произошла ошибка при скачивании: {e}")
        return None

# Пример использования
video_url = 'https://rutube.ru/video/09ca9654136855453291e95655d266d6/'
output_path = '/Users/egor/Downloads'
download_rutube_video(video_url, output_path)
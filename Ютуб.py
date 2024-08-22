import yt_dlp

def download_high_res_video(youtube_url, output_path='.'):
    try:
        # Опции для загрузки
        ydl_opts = {
            'format': '614+140',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegMerger',
            }],
            'merge_output_format': 'mp4',
        }

        # Скачивание видео
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
            print("Скачивание завершено!")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

video_url = 'https://www.youtube.com/watch?v=gHQ_QvDhs1A'
download_high_res_video(video_url, output_path='/Users/egor/Downloads')
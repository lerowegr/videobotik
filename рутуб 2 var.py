import yt_dlp


def download_mp4_video(youtube_url, output_path='.'):
    """
    Скачивает видео с указанного URL в формате MP4 с заданным разрешением.
    Если точное разрешение недоступно, выбирает ближайшее.
    """

    try:
        # Получаем информацию о доступных форматах
        ydl_opts = {
            'listformats': True,
            'skip_download': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=False)

        # Фильтруем только MP4 видео
        video_formats = [f for f in info_dict['formats'] if f['ext'] == 'mp4' and 'height' in f]
        audio_formats = [f for f in info_dict['formats'] if f['ext'] == 'm4a' or f['ext'] == 'aac']

        # Сортируем форматы по высоте видео (разрешение) в порядке возрастания
        video_formats.sort(key=lambda x: x['height'])

        target_resolution = input("Введите необходимое разрешение:")

        # Поиск ближайшего подходящего разрешения
        selected_video_format = None
        for fmt in video_formats:
            if fmt['height'] >= int(target_resolution[:-1]):
                selected_video_format = fmt
                break

        # Если точное разрешение не найдено, используем ближайшее большее
        if not selected_video_format and video_formats:
            selected_video_format = video_formats[-1]  # берем максимальное доступное

        # Если доступных форматов нет
        if not selected_video_format:
            raise ValueError("Не найдено подходящего видеоформата в MP4")

        # Выбираем лучший доступный аудиоформат
        selected_audio_format = audio_formats[0] if audio_formats else None

        # Формируем команду скачивания
        format_string = f"{selected_video_format['format_id']}+{selected_audio_format['format_id']}" if selected_audio_format else \
        selected_video_format['format_id']

        ydl_opts = {
            'format': format_string,
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegMerger',
            }],
            'merge_output_format': 'mp4',
            'ffmpeg_location': r"C:\Users\Егор\Documents\GitHub\videobotik\ffmpeg.exe",
        }

        # Скачиваем и объединяем видео и аудио
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
            print("Скачивание завершено!")

    except Exception as e:
        print(f"Произошла ошибка при скачивании: {e}")


# Пример использования
video_url = 'https://rutube.ru/video/fd07e0c992217a741f55399cc5c59e1b/'
download_mp4_video(video_url, output_path=r"C:\Users\Егор\Downloads")

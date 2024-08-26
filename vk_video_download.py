import threading
import tkinter as tk
from tkinter import ttk, filedialog
import yt_dlp
from datetime import datetime

class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.configure(bg="#f0f0f0")
        for index in range(3):
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)
        self.setup_styles()
        self.setup_widgets()
        self.save_directory = ""

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam')

        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=("Helvetica", 11))
        style.configure('TButton', font=("Helvetica", 10), padding=6, relief="flat")
        style.configure('Accent.TButton', foreground='#ffffff', background='#0078D7', font=("Helvetica", 10, "bold"))
        style.configure('TEntry', font=("Helvetica", 11))
        style.configure('TProgressbar', thickness=20)

    def setup_widgets(self):
        self.widgets_frame = ttk.Frame(self, padding=(20, 20, 20, 20))
        self.widgets_frame.grid(row=0, column=0, padx=10, pady=(25, 0), sticky="nsew")
        self.widgets_frame.columnconfigure(index=0, weight=1)

        self.label = ttk.Label(
            self.widgets_frame,
            text="Вставьте ссылку на видео",
            justify="center",
            font=("Helvetica", 14, "bold"),
        )
        self.label.grid(row=0, column=0, padx=10, pady=15, sticky="n")

        self.entry_nm = ttk.Entry(self.widgets_frame, font=("Helvetica", 12))
        self.entry_nm.grid(row=1, column=0, columnspan=10, padx=(10, 10), ipadx=150, ipady=5, pady=(0, 10), sticky="ew")
        self.entry_nm.bind('<KeyRelease>', self.on_key_release)

        self.quality_label = ttk.Label(
            self.widgets_frame,
            text="Выберите качество видео",
            justify="center",
            font=("Helvetica", 12),
        )
        self.quality_label.grid(row=2, column=0, padx=10, pady=(10, 5), sticky="n")

        self.quality_combo = ttk.Combobox(self.widgets_frame, values=[], font=("Helvetica", 11))
        self.quality_combo.grid(row=3, column=0, padx=(10, 10), ipadx=50, pady=(0, 10), sticky="ew")
        self.quality_combo.bind('<<ComboboxSelected>>', self.on_quality_selected)

        self.audio_quality_label = ttk.Label(
            self.widgets_frame,
            text="Выберите качество аудио",
            justify="center",
            font=("Helvetica", 12),
        )
        self.audio_quality_label.grid(row=4, column=0, padx=10, pady=(10, 5), sticky="n")

        self.audio_quality_combo = ttk.Combobox(self.widgets_frame, values=[], font=("Helvetica", 11))
        self.audio_quality_combo.grid(row=5, column=0, padx=(10, 10), ipadx=50, pady=(0, 10), sticky="ew")
        self.audio_quality_combo.bind('<<ComboboxSelected>>', self.on_quality_selected)

        self.bt_frame = ttk.Frame(self.widgets_frame, padding=(0, 0, 0, 0))
        self.bt_frame.grid(row=6, column=0, padx=(10, 10), pady=0, columnspan=10, sticky="ew")

        self.analyze_button = ttk.Button(
            self.bt_frame, text="Анализ видео", style="Accent.TButton", command=self.analyze_video, state=tk.DISABLED
        )
        self.analyze_button.grid(row=0, column=0, ipadx=30, padx=5, pady=(10, 5), sticky="n")

        self.directory_button = ttk.Button(
            self.bt_frame, text="Выбрать директорию", style="Accent.TButton", command=self.choose_directory, state=tk.DISABLED
        )
        self.directory_button.grid(row=0, column=1, ipadx=30, padx=5, pady=(10, 5), sticky="n")

        self.accentbutton = ttk.Button(
            self.bt_frame, text="Скачать видео", style="Accent.TButton", command=self.get_directory_string, state=tk.DISABLED
        )
        self.accentbutton.grid(row=0, column=2, ipadx=30, padx=5, pady=(10, 5), sticky="n")

        self.bt_frame.columnconfigure(index=0, weight=1)
        self.bt_frame.columnconfigure(index=1, weight=1)
        self.bt_frame.columnconfigure(index=2, weight=1)

        self.status_label = ttk.Label(
            self.widgets_frame,
            text=" ",
            justify="center",
            font=("Helvetica", 10),
        )
        self.status_label.grid(row=7, column=0, padx=0, pady=15, sticky="n")

        self.progress = ttk.Progressbar(self.widgets_frame, mode='determinate')
        self.progress.grid(row=8, column=0, padx=10, pady=(0, 10), sticky="ew")

    def choose_directory(self):
        self.save_directory = filedialog.askdirectory()
        if self.save_directory:
            self.status_label.configure(text=f"Сохранение в: {self.save_directory}")
            self.accentbutton.config(state=tk.NORMAL)

    def analyze_video(self):
        video_urls = self.entry_nm.get().strip().split(',')
        video_urls = [url.strip() for url in video_urls if url.strip()]
        if not video_urls:
            self.status_label.configure(text="Вы не ввели ссылку на видео")
            return

        available_resolutions, available_audio_qualities = self.get_available_formats(video_urls[0])
        if not available_resolutions or not available_audio_qualities:
            self.status_label.configure(text=f"Форматы недоступны для {video_urls[0]}. Пропуск.")
            return

        self.quality_combo['values'] = available_resolutions
        self.audio_quality_combo['values'] = available_audio_qualities
        self.quality_combo.current(0)
        self.audio_quality_combo.current(0)

        self.status_label.configure(text="Анализ завершён. Можно выбрать настройки и директорию.")
        self.directory_button.config(state=tk.NORMAL)

    def on_key_release(self, event):
        if self.entry_nm.get().strip():
            self.analyze_button.config(state=tk.NORMAL)
        else:
            self.analyze_button.config(state=tk.DISABLED)
            self.directory_button.config(state=tk.DISABLED)
            self.accentbutton.config(state=tk.DISABLED)

    def on_quality_selected(self, event):
        if self.quality_combo.get() and self.audio_quality_combo.get():
            self.directory_button.config(state=tk.NORMAL)

    def get_available_formats(self, video_url):
        try:
            ydl_opts = {'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                formats = info.get('formats', [])

                # Списки для хранения найденных разрешений и аудиокачеств
                available_resolutions = set()
                available_audio_qualities = set()

                for f in formats:
                    if f.get('vcodec') != 'none':
                        resolution = f.get('height')
                        if resolution:
                            available_resolutions.add(f"{resolution}p")
                    if f.get('acodec') != 'none':
                        abr = f.get('abr')
                        if abr:
                            if abr < 64:
                                available_audio_qualities.add('very low')
                            elif abr < 128:
                                available_audio_qualities.add('low')
                            elif abr < 192:
                                available_audio_qualities.add('medium')
                            elif abr < 256:
                                available_audio_qualities.add('high')
                            else:
                                available_audio_qualities.add('ultra')

                # Определение правильного порядка сортировки
                ordered_resolutions = sorted(
                    available_resolutions, key=lambda x: int(x.replace('p', ''))
                )
                ordered_audio_qualities = sorted(
                    available_audio_qualities,
                    key=lambda x: ['very low', 'low', 'medium', 'high', 'ultra'].index(x)
                )

                return ordered_resolutions, ordered_audio_qualities
        except Exception as e:
            print(f"Произошла ошибка при получении форматов: {str(e)}")
            return [], []

    def get_directory_string(self):
        video_urls = self.entry_nm.get().strip().split(',')
        video_urls = [url.strip() for url in video_urls if url.strip()]
        if not video_urls:
            self.status_label.configure(text="Вы не ввели ссылку на видео")
            return

        if not self.save_directory:
            self.status_label.configure(text="Выберите директорию для сохранения видео")
            return

        selected_quality = self.quality_combo.get()
        selected_audio_quality = self.audio_quality_combo.get()

        for video_url in video_urls:
            try:
                t = threading.Thread(target=self.download_video, args=(video_url, selected_quality, selected_audio_quality))
                t.start()
            except Exception as e:
                self.status_label.configure(text=f"Произошла ошибка: {str(e)}")

    def download_video(self, video_url, quality, audio_quality):
        self.status_label.configure(text=f"Загрузка началась для {video_url}...")
        try:
            resolution_map = {
                '144p': 'dash_sep-1',
                '240p': 'dash_sep-2',
                '360p': 'dash_sep-3',
                '480p': 'dash_sep-4',
                '720p': 'dash_sep-5',
                '1080p': 'dash_sep-6',
                '1440p': 'dash_sep-7',
                '2160p': 'dash_sep-8',
            }

            audio_quality_map = {
                'very low': 'dash_sep-7',
                'low': 'dash_sep-8',
                'medium': 'dash_sep-9',
                'high': 'dash_sep-10',
                'ultra': 'dash_sep-11',
            }

            video_format = resolution_map.get(quality, 'bestvideo')
            audio_format = audio_quality_map.get(audio_quality, 'bestaudio')

            ydl_opts = {
                'format': f'{video_format}+{audio_format}[ext=m4a]',
                'outtmpl': f'{self.save_directory}/%(title)s_%(upload_date)s.mp4',
                'quiet': True,
                'merge_output_format': 'mp4',
                'progress_hooks': [self.my_hook],
                'logger': MyLogger(),
                # Убираем 'download_archive' или используем другое имя файла
                # 'download_archive': 'new_archive.txt'  # или просто удалите эту строку
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
                self.status_label.configure(text=f"Видео {video_url} успешно скачано.")
        except Exception as e:
            self.status_label.configure(text=f"Произошла ошибка: {str(e)}")

    def my_hook(self, d):
        if d['status'] == 'downloading':
            percent = float(d['_percent_str'].replace('%', '').strip())
            root.after(0, lambda: self.update_progress(percent))
        elif d['status'] == 'finished':
            root.after(0, lambda: self.update_progress(100))

    def update_progress(self, percent):
        self.progress['value'] = percent
        self.status_label.configure(text=f"Скачиваем... {percent:.2f}% ")

    def on_enter_pressed(self, event):
        self.get_directory_string()


class MyLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


if __name__ == "__main__":
    root = tk.Tk()
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    w = w // 2
    h = h // 2
    w = w - 200
    h = h - 200
    root.geometry('680x450+{}+{}'.format(w, h))
    root.resizable(False, False)
    root.title("Скачать видео с VK.com")
    root.iconbitmap('theme/icon.ico')
    root.tk.call("source", "theme/vk_theme.tcl")
    root.tk.call("set_theme", "light")
    app = App(root)
    app.pack(fill="both", expand=True)
    root.update()
    root.mainloop()

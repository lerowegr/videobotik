import requests
from bs4 import BeautifulSoup
import re


def get_video_url(video_id):
    url = f"https://vk.com/video{video_id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Поиск ссылки на видео через регулярные выражения
    video_url_match = re.search(r'https://[^"]+\.vkuservideo\.net/[^"]+', response.text)
    if video_url_match:
        video_url = video_url_match.group(0)
        return video_url
    return None


def download_video(video_url, filename):
    response = requests.get(video_url)
    with open(filename, 'wb') as file:
        file.write(response.content)


if __name__ == "__main__":
    video_id = input("Enter the VK video ID (format: user_id_video_id): ")
    video_url = get_video_url(video_id)
    if video_url:
        filename = input("Enter the filename to save the video (e.g., video.mp4): ")
        download_video(video_url, filename)
        print("Video downloaded successfully!")
    else:
        print("Failed to get video URL.")
import requests
import os
import datetime
import shutil
from tqdm import tqdm
from yt_dlp import YoutubeDL




def get_music_urls(name):
    url = f"https://www.youtube.com/results?search_query={name}"
    response = requests.get(url)
    html = response.text
    start = html.find('watch?v=') + 8
    end = start + 11
    return 'https://www.youtube.com/watch?v=' + html[start:end]


def get_all_music_urls(names):
    urls = []
    for name in names:
        urls.append(get_music_urls(name))
    return urls

def download_music(names, session):
    urls = get_all_music_urls(names)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '../music/' + session + '/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        for url in tqdm(urls):
            ydl.download([url])

def clean_files():
    path = "../music"
    now = datetime.datetime.now()
    try:
        for folder in os.listdir(path):
            folder_path = os.path.join(path, folder)
            if os.path.isdir(folder_path):
                modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(folder_path))
                delta = now - modification_time
                if delta.total_seconds() > 60:
                    try:
                        shutil.rmtree(folder_path)
                        os.remove(folder_path + '.zip')
                        print(f'Usunięto folder {folder_path}')
                    except Exception as e:
                        print(f'Błąd podczas usuwania folderu {folder_path}: {e}')
    except Exception as e:
        print(("nie znaleziono folderu music"))
        os.makedirs(path)
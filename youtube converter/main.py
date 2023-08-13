import os
import keyboard
import pyautogui
import pyperclip
import re
import subprocess
from plyer import notification

# Konstanten
ADDRESS_FIELD_COORDS = (400, 50)
HOTKEY = 'ctrl+alt+d'
DOWNLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'Downloads')

def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_icon=None,
        timeout=10,
    )

def is_valid_youtube_link(link):
    """Überprüft, ob der Link ein gültiger YouTube-Link ist."""
    pattern = r'^https:\/\/www\.youtube\.com\/watch\?v=\w+(&\w+=\w+)*'
    return bool(re.match(pattern, link))

def get_browser_url():
    """Holt die aktuelle URL aus dem Adressfeld des Browsers."""
    pyautogui.click(*ADDRESS_FIELD_COORDS)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    return pyperclip.paste()

def download_video_from_url(url):
    """Lädt ein Video von einer gegebenen URL als MP3 herunter."""
    cmd = [
        'yt-dlp',
        url,
        '-o', os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        '--extract-audio',
        '--audio-format', 'mp3'
    ]
    subprocess.run(cmd)

def download_video():
    try:
        link = get_browser_url()
        if not is_valid_youtube_link(link):
            show_notification('Fehler beim Download', 'Der Link ist kein gültiger YouTube-Link.')
            return

        show_notification('Download gestartet', 'Download wird in Downloads gespeichert')
        download_video_from_url(link)
        os.startfile(DOWNLOAD_FOLDER)
    except Exception as e:
        show_notification('Fehler beim Download', f'Es ist ein Fehler aufgetreten: {str(e)}')
        print(str(e))


keyboard.add_hotkey(HOTKEY, download_video)

while True:
    keyboard.wait()

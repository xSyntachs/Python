import os
import keyboard
import pyautogui
import pyperclip
import re
import subprocess
import time
from plyer import notification

# Konstanten
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
    x, y = pyautogui.position()  # Aktuelle Mausposition holen
    pyautogui.click(x, y)  # An der aktuellen Mausposition klicken
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
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

def main():
    # Überprüfen, ob yt-dlp installiert ist
    try:
        subprocess.run(['yt-dlp', '--version'], check=True)
    except subprocess.CalledProcessError:
        print("Bitte installieren Sie yt-dlp.")
        return

    keyboard.add_hotkey(HOTKEY, download_video)
    keyboard.wait()

if __name__ == "__main__":
    main()

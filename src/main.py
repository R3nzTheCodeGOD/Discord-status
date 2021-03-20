import spotipy
import spotipy.util as util
import requests
import time
import configparser
import sys
import colorama
import os
import codecs
colorama.init()

__author__: str = 'Erdem Yılmaz'
__version__: str = '1.0.0'

class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def draw_bar(prog_max:int, prog_current: int, prog_bar_lenght: int=25) -> str:
    "Return progress bar"
    prog_bar_str: str = ''
    percentage: float = prog_current / prog_max

    for i in range(prog_bar_lenght):
        if (percentage < 1 / prog_bar_lenght * i):
            prog_bar_str += '□'
        else:
            prog_bar_str += '■'
    return prog_bar_str

def get_token() -> str:
    "Get Spotify Token"
    token = util.prompt_for_user_token(username, 'user-read-currently-playing', client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    return token

def change_status(artist: str="", song: str="", progress_time: int=0, progress_max: int=0, music=True) -> None:
    "Change Discord Status"
    if music is True:
        setting: dict = {
            'status': discord_status,
            'custom_status': {'text': f"{song} - {artist} {draw_bar(prog_max=progress_max, prog_current=progress_time)} ⇆　　◁　　❚❚　　▷　　↻"}
        }
    else:
        setting: dict = {
            'status': discord_status,
            'custom_status': {
                'text': f'{no_music_text} □■□■□■□■□■□■□■□■□■□■□■□■□ ⇆　　◁　　▶　　▷　　↻'
            }
        }
    request.patch("https://canary.discordapp.com/api/v6/users/@me/settings", headers=headers, json=setting, timeout=10)

def main() -> None:
    "MainFunc"
    spotify = spotipy.Spotify(auth=get_token())
    current_track: dict = spotify.current_user_playing_track()
    while True:
        try:
            current_track: dict = spotify.current_user_playing_track()
            if current_track is None:
                change_status(music=False)
                continue
            if current_track['is_playing'] is False:
                change_status(music=False)

            else:
                artist = current_track['item']['artists'][0]['name']
                song = current_track['item']['name']
                progres_time = current_track['progress_ms']
                progres_max = current_track['item']['duration_ms']
                change_status(artist=artist, song=song, progress_time=progres_time, progress_max=progres_max, music=True)

            time.sleep(loop_time)
        except Exception as err:
            spotify = spotipy.Spotify(auth=get_token())
            print(color.WARNING + "[INFO] Reset Token" + color.ENDC)
            print(err)
            continue

if __name__ == "__main__":
    request = requests.Session()
    os.system("cls")
    os.system("@echo off")
    cfg = configparser.ConfigParser()
    cfg.read_file(codecs.open("config.ini", "r", "utf8"))
    username: str = str(cfg.get("account", "username"))
    client_id: str = str(cfg.get("account", "client_id"))
    client_secret: str = str(cfg.get("account", "client_secret"))
    redirect_uri: str = str(cfg.get("account", "redirect_uri"))
    headers: dict = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7',
        'Content-Type': 'application/json',
        'Authorization': str(cfg.get("account", "discord_token"))
    }
    discord_status: str = str(cfg.get("general", "discord_status"))
    no_music_text: str = str(cfg.get("general", "no_music_text"))
    loop_time: float = float(cfg.get("general", "loop_time"))
    print(color.BOLD + color.OKGREEN + f"""
     ____  _____           _____ _           ____          _       ____  ___  ____  
    |  _ \|___ / _ __  ___|_   _| |__   ___ / ___|___   __| | ___ / ___|/ _ \|  _ \ 
    | |_) | |_ \| '_ \|_  / | | | '_ \ / _ \ |   / _ \ / _` |/ _ \ |  _| | | | | | |
    |  _ < ___) | | | |/ /  | | | | | |  __/ |__| (_) | (_| |  __/ |_| | |_| | |_| |
    |_| \_\____/|_| |_/___| |_| |_| |_|\___|\____\___/ \__,_|\___|\____|\___/|____/

                    {color.OKCYAN + "GitHub: https://github.com/R3nzTheCodeGOD" + color.ENDC}
    """ + color.ENDC)
    try:
        os.open(f".cache-{username}", 1)
    except FileNotFoundError:
        print(color.BOLD + color.WARNING + "Info: When you use the program for the first time, copy and paste the URL of the website opened in your browser into the console." + color.ENDC)
    main()
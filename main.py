import json
import discord
import re
from yt_dlp import YoutubeDL
from asyncio import sleep
import os
from ytmusic import get_video
import sys
from settings import PATH_TO_TOKEN
from JSON import readJSON, writeJSON


BASE_DIR = os.path.split(os.path.abspath(__file__))[0] + "\\"


#TEXT_SERVER_ID = 760581470565433425

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False'}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


def compare(r, text):  # Compare function
    match = re.match(r, str(text))
    if match is not None:
        if match.group(0) != '': return True
    return False

# Making Client class
class Client(discord.Client):
    def __init__(self, server):
        super(Client, self).__init__()
        self.server = server;

        try:
            self.playlists = readJSON(self.server)
        except:
            self.playlists = {}
            writeJSON(self.server, self.playlists)

        self.queue = []

    async def add_queue(self, url):  # Adding song to a queue
        self.queue.append(url)

    async def play(self, voice_channel):
        global vc

        print(f"[INFO] playing to {voice_channel}")

        try:
            vc = await voice_channel.connect()
        except:
            print('[WARNING] Already have connected or cannot connect to the server.')
            if not vc: return

        if vc.is_playing():
            print("[WARNING] Vc is playing but you try to start it again.")
        else:
            while len(self.queue) > 0:
                try:
                    URL = self.queue[0]
                    with YoutubeDL(YDL_OPTIONS) as ydl:
                        info = ydl.extract_info(URL, download=False)

                    url = info['formats'][1]['url']
                    print(info['formats'][:5])
                    vc.play(discord.FFmpegPCMAudio(executable=BASE_DIR+"ffmpeg\\ffmpeg.exe", source = url, **FFMPEG_OPTIONS))

                    await self.sent_message(f"Now playing: {URL}")
                    self.now_playing = URL
                    while vc.is_playing() or vc.is_paused():
                        await sleep(1)
                except:
                    await self.sent_message("I can`t do this!1")
                finally:
                    try:
                        self.queue = self.queue[1:]
                    except:
                        pass
            try:
                if not vc.is_paused():
                    await vc.disconnect()
            except:
                await self.sent_message("I can`t do this!2")

    async def docommand(self, message):
        global vc

        if compare("^!play ", message.content) or compare("^!p ", message.content):
            if compare("^!play http*", message.content) or compare("^!p http*", message.content):
                url = message.content.split()[1]
                await self.add_queue(url)
            else:
                try:
                    playlist = self.playlists[" ".join(message.content.split()[1:])]
                    for song in playlist:
                        await self.add_queue(song)
                except:
                    try:
                        name = " ".join(message.content.split()[1:])
                        song = get_video(name)
                        await self.add_queue(song)
                    except:
                        print("[ERROR] Cannot find valid video.")
            try:
                if not vc.is_playing():
                    await self.play(message.author.voice.channel)
            except:
                try:
                    await self.play(message.author.voice.channel)
                except:
                    print("[ERROR] Something went wrong while connecting to a voie channel.")

        elif compare("^!queue", message.content) or compare("^!q", message.content):
            if len(self.queue) == 0:
                await self.sent_message("Queue is empty")
            else:
                await self.sent_message("Queue:\n" + "\n".join([str(i+1)+". "+name for i, name in enumerate(self.queue[:5])]))

        elif compare("^!dis", message.content):
            try:
                self.queue = []
                await vc.stop()
                await vc.disconnect()
            except: pass

        elif compare("^!skip", message.content) or compare("^!s", message.content):
            try:
                await vc.stop()
                self.queue = self.queue[1:]
            except:
                pass

        elif compare("^!pause", message.content):
            try:
                await vc.pause()
            except:
                pass

        elif compare("^!resume", message.content):
            try:
                await vc.resume()
            except:
                pass

        elif compare("^!help", message.content):
            await self.sent_message(
"""I know such commands as:
1. !play smth - {!p - is the same} I will add the song you want to the queue. Instead of 'smth' you should write the url to a video on YouTube, or the name of the playlist, or the name of the song.
2. !queue - {!q - is the same} I will show the queue.
3. !skip - {!s - is the same} I will skip the current song.
4. !help - It's a help.
5. !dis - I will disconnect from server and clear queue.
6. !playlists - {!pls is the same} I will show all playlists that I know.
6.1 !playlists name - I will show the list of songs of necessary playlist. Instead of 'name' put the name of playlist.
6.2 !playlists add name - I will make a new playlist. Instead of 'name' put the name of playlist.
6.3 !playlists update url name - I will add a song to a playlist. Instead of 'url' put the url to a song, instead of 'name' put the name of playlist.
7. !pause - I will pause the current song.
8. !resume - I will resume the current song."""
            )
        elif compare("^!playlists", message.content) or compare("^!pls", message.content):
            if compare("^!playlists add *", message.content) or compare("^!pls add *", message.content):
                try:
                    playlist = " ".join(message.content.split()[2:])
                    if playlist[:6] == "https:": a=1/0
                    self.playlists.update({playlist: []})
                    writeJSON(self.server, self.playlists)
                except:
                    print("[ERROR] Something got wrong while adding a playlist.")

            elif compare("^!playlists update *", message.content) or compare("^!pls update *", message.content):
                try:
                    url = message.content.split()[2]
                    playlist = " ".join(message.content.split()[3:])
                    self.playlists[playlist].append(url)

                    writeJSON(self.server, self.playlists)
                except:
                    print("[ERROR] Something got wrong while adding a song to a playlist.")

            elif compare("^!playlists \w*", message.content) or compare("^!pls \w*", message.content):
                try:
                    playlist = " ".join(message.content.split()[1:])
                    plst = self.playlists[playlist]
                    result = " \n".join([str(i+1)+". "+name for i, name in enumerate(plst)])
                    await self.sent_message(f"In {playlist} there are:\n" + result)

                except:
                    print("[ERROR] Something got wrong while showing a playlist.")

            else:
                result = "\n".join([str(i+1)+". "+name for i, name in enumerate(self.playlists.keys())])
                await self.sent_message("I know such playlists as:\n" + result)

        else:
            await self.sent_message("Нихуя не понял, но очень интересно. Что бы узнать какие есть комманды введи !help.")

    async def sent_message(self, text):
        try:
            await self.text_channel.send(text)
        except:
            print("[ERROR] Cannot connect to unidentified text channel.")

    async def on_ready(self):
        print("Hello")

    async def on_message(self, message):
        if (message.author != self.user and self.server == message.guild.id):
            self.actions = {r"^!*": self.docommand} # Put here function that will execute if needed message will be received
            self.text_channel = message.channel
            text = message.content
            for key, value in self.actions.items():
                if compare(key, text):
                        await value(message)

# Getting token
with open(PATH_TO_TOKEN, "r") as f: token = f.read()

# Starting client

def run_server(server):
    client = Client(server)
    client.run(token)

run_server(int(sys.argv[1]))

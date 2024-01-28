import discord
import sys
from settings import PATH_TO_TOKEN


guilds = []

class Client(discord.Client):  # Client class to get all guilds
    async def on_ready(self):
        global guilds
        guilds = self.guilds
        await self.close()


def getServers():  # Getting guilds
    with open(PATH_TO_TOKEN, "r") as f: token = f.read()

    client = Client()
    client.run(token)
    
    return guilds

"""
ImageShopper Discord Bot for Image Manipulating Functionality with pillow and numpy
"""

# imports
from dotenv import load_dotenv
from typing import List
import os
import discord
import modifiers as mod
import commands

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

prefix = "!?!"

client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Image Manipulation Workshop'))
    print(f"logged in as {client.user}")

@client.event
async def on_message(message: discord.Message):
    channel = message.channel
    if message.author != client.user:
        msg: List[str] = message.content.split(prefix)
        if msg[0] == "":
            # commands
            try:
                if msg[1] == "help":
                    await commands.help_command(channel, client)
                elif msg[1] == "run":
                    await commands.run_command(message, client)
                else:
                    if not mod.img.in_sess: # prevents this from showing up when a user is in session
                        await channel.send("Unkown command, type: `!?!help` for help")
            except IndexError:
                pass
    
    
# run bot
if __name__ == '__main__':
    client.run(token)
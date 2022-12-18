"""
ImageShopper Discord Bot for Image Manipulating Functionality with pillow and numpy
"""

# imports
from dotenv import load_dotenv
import os
import discord
import asyncio
import modifiers as mod
import commands

# Bot side
def _startswith(message, cmd):
    return message.content.lower().startswith(cmd)

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
        # commands
        if _startswith(message, f"{prefix}array"):    
            await channel.send(f"heres the current array that will produce your image {chr(128512)}")    
            await channel.send(f"{mod.img.base_image}")
        elif _startswith(message, f"{prefix}help"):
            await commands.help_command(channel, client)
        elif _startswith(message, f"{prefix}run"):
            await commands.run_command(message, client)
        else:
            if not mod.img.in_sess:
                await channel.send("Unkown command, type: `!?!help` for help")
    
    
# run bot
if __name__ == '__main__':
    client.run(token)
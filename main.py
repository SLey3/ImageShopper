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
    print(f"logged in as {client.user}")

@client.event
async def on_message(message):
    channel = message.channel
    if message.author != client.user:
        # commands
        if _startswith(message, f"{prefix}hi"):    
            await channel.send("heres a numpy array 😀")
            
            
            img = mod.ImageObject()
        
            await channel.send(f"{img.base_image}")
        elif _startswith(message, f"{prefix}help"):
            await commands.help_command(channel, client)
    
    
# run bot
if __name__ == '__main__':
    client.run(token)
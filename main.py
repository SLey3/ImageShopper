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
        if message.content.lower().startswith(f"{prefix}hi"):    
            await channel.send("heres a numpy array 😀")
            
            
            img = mod.ImageObject()
        
            await channel.send(f"{img.base_image}")
    
    
# run bot
if __name__ == '__main__':
    client.run(token)
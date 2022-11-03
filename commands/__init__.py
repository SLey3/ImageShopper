# Imports
from main import client
import discord
import modifiers as mod


async def help_command(ctx):
    embed = discord.Embed(title="ImageShopper Command List",
                          description="Help is right below! Check out my functionality!"
                          color=discord.Color.blue())
    
    embed.set_author(name=client.user.name,
                     icon_url=client.user.avatar_url)
    
    help_emoji = discord.Emoji()
    help_emoji.name = ":sos:"
    
    embed_field_desc = f"""
    >>> {help_emoji} `!?!help` : Loads up this embed providing available command
    """
    
    
    embed.add_field(name="Commands:", 
                    value=embed_field_desc)
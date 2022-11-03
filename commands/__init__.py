# Imports
import discord
import modifiers as mod


async def help_command(ctx, client):
    embed = discord.Embed(title="ImageShopper Command List",
                          description="Help is right below! Check out my functionality!",
                          color=discord.Color.blue())
    
    embed.set_author(name=client.user.name,
                     icon_url=client.user.avatar_url)
    
    embed_field_desc = f"""
    >>> <:sos:1037764237411487808>  `!?!help` : Loads up this embed providing available commands
    """
    
    
    embed.add_field(name="Commands:", 
                    value=embed_field_desc)
    
    await ctx.send(embed=embed)
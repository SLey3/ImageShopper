# Imports
import discord
import modifiers as mod
import asyncio


async def help_command(ctx: discord.TextChannel, client: discord.Client):
    embed = discord.Embed(title="ImageShopper Command List",
                          description="Help is right below! Check out my functionality!",
                          color=discord.Color.blue())
    
    embed.set_author(name=client.user.name,
                     icon_url=client.user.avatar_url)
    
    embed_field_desc = """
    >>> <:sos:1037764237411487808>  `!?!help` : Loads up this embed providing available commands
    〚〛 `!?!array` : Shows current image array
    <:star:1037879151065038848> `!?init` : Loads Tool Initialization Menu. Must be run before functionality can take place
    """
    
    
    embed.add_field(name="Commands:", 
                    value=embed_field_desc)
    
    await ctx.send(embed=embed)

async def init_command(msg: discord.Message, client: discord.Client):
    ctx: discord.TextChannel = msg.channel
    
    embed = discord.Embed(title="Initialize Image", 
                          description="Select which image you want to edit",
                          color=discord.Color.dark_red())

    embed.set_author(name=client.user.name,
                     icon_url=client.user.avatar_url)

    embed_field_desc = """
    >>> 📂 : Click this to open file dialog
    """

    sent_embed = await ctx.send(embed=embed)
    await sent_embed.add_reaction("📂")

    def _check(rctn, user):
        return user.id == msg.author.id and str(rctn) == "📂"

    try:
        rctn, reacted = await client.wait_for("reaction_add", check=_check, timeout=30)
    except asyncio.TimeoutError:
        pass
    
    if reacted:
        mod.init_file()
        
        await ctx.send(mod.img.base_image)
        mod.img.image.show()

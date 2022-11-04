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
    <:star:1037879151065038848> `!?!run` : Loads Tool Initialization Menu. Must be run before functionality can take place
    """
    
    
    embed.add_field(name="Commands:", 
                    value=embed_field_desc)
    
    await ctx.send(embed=embed)

async def run_command(msg: discord.Message, client: discord.Client):
    ctx: discord.TextChannel = msg.channel
    
    embed = discord.Embed(title="Initialize Image", 
                          description="Select which image you want to edit",
                          color=discord.Color.dark_red())

    embed.set_author(name=client.user.name,
                     icon_url=client.user.avatar_url)

    embed_field_desc = """
    >>> 📂 : Click this to open file dialog
    """

    embed.add_field(name="__**Reactions**__", value=embed_field_desc)

    sent_embed: discord.Message = await ctx.send(embed=embed)
    await sent_embed.add_reaction("📂")

    def _check(rctn, user):
        return user.id == msg.author.id and str(rctn) == "📂"

    try:
        rctn, reacted = await client.wait_for("reaction_add", check=_check, timeout=30)
    except asyncio.TimeoutError:
        pass
    
    if reacted:
        await  sent_embed.remove_reaction("📂", reacted)
        mod.init_file()

        main_functionality_menu_embed = discord.Embed(title="Select Functionality",
                                                      color=discord.Color.purple())

        main_functionality_menu_embed.set_author(name=client.user.name,
                                                 icon_url=client.user.avatar_url)

        main_functionality_menu_embed.set_thumbnail(url=f"attachment://{mod.img.image.filename}")
        
        desc = """
        >>> <:arrow_up_down:1038150600510165093> : Flip vertically
        <:left_right_arrow:1038150773730713661> : Flip vertically
        <:grey_exclamation:1038150998549598288> : Grayscale
        <:person_surfing:1038151315735449641> : Equalize
        """

        main_functionality_menu_embed.add_field(name="__**Reactions:**__", value=desc)

        sent_embed: discord.Message = await ctx.send(file=mod.img.discord_file, embed=main_functionality_menu_embed)


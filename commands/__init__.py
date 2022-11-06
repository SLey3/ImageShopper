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
        rctn, reacted = await client.wait_for("reaction_add", check=_check, timeout=10)
    except asyncio.TimeoutError:
        pass
    
    if reacted:
        await sent_embed.remove_reaction("📂", reacted)
        mod.init_file()

        await main_functionality_prompt(msg, ctx, client)
        

async def main_functionality_prompt(msg: discord.Message, ctx: discord.TextChannel, client: discord.Client):
    main_functionality_menu_embed = discord.Embed(title="Select Functionality",
                                                    color=discord.Color.purple())

    main_functionality_menu_embed.set_author(name=client.user.name,
                                                icon_url=client.user.avatar_url)

    main_functionality_menu_embed.set_thumbnail(url=f"attachment://{mod.img.image.filename}")
    
    reactions = [
        8597,
        8596,
        10069,
        127940
    ]
    
    desc = f"""
    >>> {chr(reactions[0])} : Flip vertically
    {chr(reactions[1])} : Flip vertically
    {chr(reactions[2])} : Grayscale
    {chr(reactions[3])} : Equalize
    """

    main_functionality_menu_embed.add_field(name="__**Reactions:**__", value=desc)

    sent_embed: discord.Message = await ctx.send(file=mod.img.discord_file, embed=main_functionality_menu_embed)
    await sent_embed.add_reaction(chr(reactions[0]))
    await sent_embed.add_reaction(chr(reactions[1]))
    await sent_embed.add_reaction(chr(reactions[2]))
    await sent_embed.add_reaction(chr(reactions[3]))
    
    def _check(rctn, user):
        return user.id == msg.author.id and ord(rctn.emoji) in reactions 
    
    rctn, reacted = None, None # to avoid UnboundLocarError
    
    try:
        rctn, reacted = await client.wait_for("reaction_add", check=_check, timeout=10)
    except asyncio.TimeoutError:
        pass
    
    if reacted:
        await sent_embed.remove_reaction(rctn, reacted)
        
        if rctn.emoji == chr(reactions[0]):
            # flip vertical
            print("flip vertical")
        elif rctn.emoji == chr(reactions[1]):
            # flip horizontal
            print("flip horizontal")
        elif rctn.emoji == chr(reactions[2]):
            # grayscale
            print("grayscale")
        elif rctn.emoji == chr(reactions[3]):
            # equalize
            print("equalize")
        else:
            print("None. Something wrong happened")
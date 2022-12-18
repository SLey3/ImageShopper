# Imports
import discord
import modifiers as mod
import asyncio
import os


async def help_command(ctx: discord.TextChannel, client: discord.Client):
    embed = discord.Embed(title="ImageShopper Command List",
                          description="Help is right below! Check out my functionality!",
                          color=discord.Color.blue())
    
    embed.set_author(name=client.user.name,
                     icon_url=client.user.avatar_url)


    reactions = [
        127384,
        11088
    ]
    
    embed_field_desc = f"""
    >>> {chr(reactions[0])} `!?!help` : Loads up this embed providing available commands
    {chr(reactions[1])} `!?!run` : Loads Tool Initialization Menu. Must be run before functionality can take place
    """
    
    
    embed.add_field(name="Commands:", 
                    value=embed_field_desc)
    
    await ctx.send(embed=embed)

async def run_command(msg: discord.Message, client: discord.Client):
    ctx: discord.TextChannel = msg.channel
    
    mod.img.in_sess = True

    embed = discord.Embed(title="Initialize Image", 
                          description="Select which image you want to edit",
                          color=discord.Color.dark_red())

    embed.set_author(name=client.user.name,
                     icon_url=client.user.avatar_url)

    embed_field_desc = """
    >>> Send an attachment containing the image you would wish to edit.
    """

    embed.add_field(name="__**Description:**__", value=embed_field_desc)

    sent_embed: discord.Message = await ctx.send(embed=embed)
    

    try:
        msg = await client.wait_for("message", timeout=60)
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond!")
        return
    
    if msg:
        
        save_embed = discord.Embed(title="Save Image",
                                   description="Decide whether you want to save the image after your finished.",
                                   color=discord.Color.blue())

        save_embed.set_author(name=client.user.name,
                              icon_url=client.user.avatar_url)

        reactions = [
            9989,
            10060
        ]
        save_embed_desc = f"""
        >>> {chr(reactions[0])} : Yes
        {chr(reactions[1])} : No
        """

        save_embed.add_field(name="__**Reactions:**__", value=save_embed_desc)

        sent_save_embed: discord.Message = await ctx.send(embed=save_embed)

        await sent_save_embed.add_reaction(chr(reactions[0]))
        await sent_save_embed.add_reaction(chr(reactions[1]))

        def _check(rctn, user):
            return user.id == msg.author.id and ord(rctn.emoji) in reactions 

        rctn, reacted = await client.wait_for("reaction_add", check=_check)

        if reacted:
            await sent_save_embed.remove_reaction(rctn, reacted)

            if rctn.emoji == chr(reactions[0]): # Yes
                mod.img.save = True

        res = await mod.init_file(msg.attachments[0], ctx)
        if res:
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
        127940,
        128295
    ]
    
    desc = f"""
    >>> {chr(reactions[0])} : Flip vertically
    {chr(reactions[1])} : Flip horizontal
    {chr(reactions[2])} : Grayscale
    {chr(reactions[3])} : Equalize
    {chr(reactions[4])} : View current image array
    """

    main_functionality_menu_embed.add_field(name="__**Reactions:**__", value=desc)

    in_run = True
    while in_run:

        sent_embed: discord.Message = await ctx.send(embed=main_functionality_menu_embed)
        await sent_embed.add_reaction(chr(reactions[0]))
        await sent_embed.add_reaction(chr(reactions[1]))
        await sent_embed.add_reaction(chr(reactions[2]))
        await sent_embed.add_reaction(chr(reactions[3]))
        await sent_embed.add_reaction(chr(reactions[4]))
        
        def _check(rctn, user):
            return user.id == msg.author.id and ord(rctn.emoji) in reactions 
        
        rctn, reacted = None, None # to avoid UnboundLocalError
        
        try:
            rctn, reacted = await client.wait_for("reaction_add", check=_check, timeout=25)
        except asyncio.TimeoutError:
            await ctx.send("you took too long to respond!")
            return
        
        if reacted:
            await sent_embed.remove_reaction(rctn, reacted)
            
            if rctn.emoji == chr(reactions[0]):
                # flip vertical
                mod.flip_vertical()
            elif rctn.emoji == chr(reactions[1]):
                # flip horizontal
                mod.flip_horizontal()
            elif rctn.emoji == chr(reactions[2]):
                # grayscale
                print("grayscale")
            elif rctn.emoji == chr(reactions[3]):
                # equalize
                print("equalize")
            else:
                await ctx.send(mod.img.base_image)


            def check(msg):
                return msg.channel.id == ctx.id

            await ctx.send("Do you want to stop (Y or N)")

            res: discord.Message = await client.wait_for('message', check=check)

            if res.content.capitalize() == "Y":

                if mod.img.save:
                    file = discord.File(mod.img.temp_file_fp, filename=mod.img.image_name, spoiler=True)


                    await ctx.send(f"**__RESULT:__**")
                    await ctx.send(file=file)

                os.remove(mod.img.temp_file_fp)
                mod.img.discord_file.close()
                mod.img.reset_to_defaults()

                in_run = False
            elif res.content.capitalize() == "N":
                await ctx.send("Do you want to save this current rendition? (Y or N)")

                res: discord.Message = await client.wait_for("message", check=check)

                if res.content.capitalize() == "Y":
                    mod.img.discord_file.close()
                    file = discord.File(mod.img.temp_file_fp, filename=mod.img.image_name, spoiler=True)

                    await ctx.send(f"**__CURRENT RENDITION__**")
                    await ctx.send(file=file)
                    file.spoiler = False
                    mod.img.discord_file = file


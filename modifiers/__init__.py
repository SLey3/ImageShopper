# Imports
from PIL import Image, ImageSequence, ImageOps
import numpy as np
import attr
import discord
import requests
import shutil
import os

ALLOWED_FILE_EXT = [
    "*.jpg",
    "*.jpeg",
    "*.jpe",
    "*.png",
    "*.gif",
    "*.webp",
    "*.tiff",
    "*.tif",
    "*.bmp",
    "*.dib",
]

FILE_EXT_BIT = {
    "MPO": np.int8,
    "JPEG": np.int8,
    "PNG": np.int64,
    "GIF": np.int8,
    "WEBP": np.int8,
    "TIFF": np.int16,
    "BMP": np.int32
}

BASE_TEMP_FP = os.path.join(os.getcwd(), "modifiers", "temp")

RGB_WHITE = (255, 255, 255,)

def _reopen():
    # reopen and configure the image
    if img.discord_file is not None:
        img.discord_file.close()
    new_image = discord.File(img.temp_file_fp)
    img.discord_file = new_image
    img.image = Image.open(img.temp_file_fp)

@attr.s(slots=True)
class ImageSettings:
    """
    Image class that contains all necessary attributes for manipulating images
    """
    image = attr.ib(default=Image.new("RGB", (250, 250), RGB_WHITE), type=Image)
    base_image = attr.ib(default=np.zeros((int(256/2), int(256/2)), dtype=np.int64), 
                   type=np.array)
    discord_file = attr.ib(default=None, type=discord.File)
    image_name = attr.ib(default=None, type=str)
    image_type = attr.ib(default="PNG", type=str)
    temp_file_fp = attr.ib(default="", type=str)
    save = attr.ib(default=False, type=bool)
    in_sess = attr.ib(default=False, type=bool)

    def reset_to_defaults(self):
        """
        reset image settings back to defaults
        """
        self.image = None
        self.base_image = np.zeros((int(256/2), int(256/2)), dtype=np.int64)
        self.discord_file.close()
        self.discord_file = None
        self.image_type = "PNG"
        self.image_name = None
        self.temp_file_fp = ""
        self.in_sess = False


img = ImageSettings()

def flip_vertical():
    """
    flips the image top to bottom or vice versa
    """
    if img.image_type == "GIF":
        new_frames = []
        new_image = Image.new("RGB", img.image.size, RGB_WHITE)

        for frame in ImageSequence.Iterator(img.image):
            new_frames.append(frame.transpose(Image.Transpose.FLIP_TOP_BOTTOM))

        new_image.save(img.temp_file_fp, save_all=True, append_images=new_frames)

        # reopen and configure the image
    else:
        img.image = img.image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        img.image.save(img.temp_file_fp)

    _reopen()
    img.base_image = np.array(img.image, dtype=FILE_EXT_BIT[img.image_type])

def flip_horizontal():
    if img.image_type == "GIF":
        new_frames = []
        new_image = Image.new("RGB", img.image.size, RGB_WHITE)
        
        for frame in ImageSequence.Iterator(img.image):
            new_frames.append(frame.transpose(Image.Transpose.FLIP_LEFT_RIGHT))

        new_image.save(img.temp_file_fp, save_all=True, append_images=new_frames) # Due to the image is a GIF file, all frames must be overwritten

    else:
        img.image = img.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        img.image.save(img.temp_file_fp)

    _reopen()
    img.base_image = np.array(img.image, dtype=FILE_EXT_BIT[img.image_type])

def grayscale():
    if img.image_type == "GIF":
        new_frames = []
        new_image = Image.new("RGB", img.image.size, RGB_WHITE)

        for frame in ImageSequence.Iterator(img.image):
            new_frames.append(frame.convert(mode="L"))
        
        new_image.save(img.temp_file_fp, save_all=True, append_images=new_frames)
    else:
        img.image = ImageOps.grayscale(img.image)
        img.image.save(img.temp_file_fp)

    _reopen()
    img.base_image = np.array(img.image, dtype=FILE_EXT_BIT[img.image_type])

def equalize():
    if img.image_type == "GIF":
        new_frames = []
        new_image = Image.new("RGB", img.image.size, RGB_WHITE)

        for frame in ImageSequence.Iterator(img.image):
            new_frames.append(ImageOps.equalize(frame))

        new_image.save(img.temp_file_fp, save_all=True, append_images=new_frames)
    else:
        img.image = ImageOps.equalize(img.image)
        img.image.save(img.temp_file_fp)

    _reopen()
    img.base_image = np.array(img.image, dtype=FILE_EXT_BIT[img.image_type])
            

async def init_file(attachment: discord.Attachment, ctx: discord.TextChannel):
    """
    Initialization portion to get and confirgure image file for :class:ImageObject
    """
    res = requests.get(attachment.url, stream=True)
    
    if res.status_code == 200:
        img.temp_file_fp = os.path.join(BASE_TEMP_FP, f"{attachment.filename}")
        with open(img.temp_file_fp, 'wb') as temp:
            shutil.copyfileobj(res.raw, temp)
    else:
        await ctx.send(f'''Failed to connect to the discord CDN, unable to process further commands untill CDN is available again.\n
        -------------------------------------------------------------------------------------------------------\n
        **__Status Code__**: {res.status_code}''')
        return False

    discord_img_file = await attachment.to_file()

    _img = Image.open(img.temp_file_fp)
    img_array = np.array(_img, dtype=FILE_EXT_BIT[_img.format])
    img.image = _img
    img.base_image = img_array
    img.image_type = _img.format
    img.image_name = _img.filename
    img.discord_file = discord_img_file
    return True
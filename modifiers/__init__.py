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

@attr.s(slots=True)
class ImageSettings:
    """
    Image class that contains all necessary attributes for manipulating images
    """
    image = attr.ib(default=None, type=Image)
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
        new_image = Image.new("RGB", img.image.size, (255, 255, 255))

        for frame in ImageSequence.Iterator(img.image):
            new_frames.append(frame.transpose(Image.Transpose.FLIP_TOP_BOTTOM))

        new_image.save(img.temp_file_fp, save_all=True, append_images=new_frames)

        # reopen and configure the image
        new_image = discord.File(img.temp_file_fp)
        img.discord_file = new_image
        img.image = Image.open(img.temp_file_fp)
    else:
        img.image = img.image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

    img.base_image = np.array(img.image, dtype=FILE_EXT_BIT[img.image_type])

def flip_horizontal():
    if img.image_type == "GIF":
        image = img.image
        new_frames = []

        new_image = Image.new("RGB", image.size, (255, 255, 255))
        for frame in ImageSequence.Iterator(image):
            new_frames.append(frame.transpose(Image.Transpose.FLIP_LEFT_RIGHT))

        new_image.save(img.temp_file_fp, save_all=True, append_images=new_frames) # Due to the image is a GIF file, all frames must be overwritten
        
        # reopen and configure the image
        new_image = discord.File(img.temp_file_fp)
        img.discord_file = new_image
        img.image = Image.open(img.temp_file_fp)

    else:
        img.image = img.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

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
                           Status Code: {res.status_code}''')
        return False

    img_file = discord.File(img.temp_file_fp, filename=attachment.filename)

    _img = Image.open(img.temp_file_fp)
    img_array = np.array(_img, dtype=FILE_EXT_BIT[_img.format])
    img.image = _img
    img.base_image = img_array
    img.image_type = _img.format
    img.image_name = _img.filename
    img.discord_file = img_file
    return True
# Imports
from PIL import Image, ImageOps
from io import BytesIO
import numpy as np
import attr
import easygui
import discord

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

@attr.s(slots=True)
class ImageObject:
    """
    Image class that contains all necessary attributes for manipulating images
    """
    image = attr.ib(default=None, type=Image)
    base_image = attr.ib(default=np.zeros((int(256/2), int(256/2)), dtype=np.int64), 
                   type=np.array)
    discord_file = attr.ib(default=None, type=discord.File)
    image_name = attr.ib(default=None, type=str)
    image_type = attr.ib(default="PNG", type=str)
    
    def convert_array_to_img(self):
        self.image = Image.fromarray(FILE_EXT_BIT[self.image_type](self.base_image*255))
        return self.image

    def reset_to_defaults(self):
        self.image = None
        self.base_image = np.zeros((int(256/2), int(256/2)), dtype=np.int64)
        self.discord_file.close()
        self.discord_file = None
        self.image_type = "PNG"
        self.image_name = None


img = ImageObject()

def flip_vertical():
    """
    flips the image top to bottom or vice versa
    """
    img.image = img.image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    img.base_image = np.array(img.image, dtype=FILE_EXT_BIT[img.image_type])

def flip_horizontal():
    if img.image_type == "GIF":
        image = img.image
        for n in range(0, image.n_frames):
            image.seek(n)
            image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    img.image = image
    img.base_image = np.array(img.image, dtype=FILE_EXT_BIT[img.image_type])

def init_file():
    """
    Initialization portion to get and confirgure image file for :class:ImageObject
    """
    file = easygui.fileopenbox("Choose image file",
                               "Open File",
                               filetypes=ALLOWED_FILE_EXT) # Issues: 
                                                            # Windows: Dialog hides behind discord fullscreen
                                                            # MacOs: Tk titled window visible, included after file dialog is removed after user either selected an image or closed out

    if file is None:
        return False

    _img = Image.open(file)
    img_array = np.array(_img, dtype=FILE_EXT_BIT[_img.format])
    img.image = _img
    img.base_image = img_array
    img.image_type = _img.format
    img.image_name = _img.filename

    dfile = discord.File(file, filename=_img.filename)

    img.discord_file = dfile
    return True
    
if __name__ == '__main__':
    img = ImageObject()
    print(img.base_image)
    res = img.convert_array_to_img()
    res.show()
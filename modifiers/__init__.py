# Imports
from PIL import Image, ImageOps
import numpy as np
import attr
import easygui

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
    image = attr.ib(default=None, type=Image)
    base_image = attr.ib(default=np.zeros((int(256/2), int(256/2)), dtype=np.int64), 
                   type=np.array)
    
    def convert_array_to_img(self):
        self.image = Image.fromarray(np.int64(self.base_image*255))
        return self.image


img = ImageObject()

def init_file():
    """
    Initialization portion to get and confirgure image file for :class:ImageObject
    """
    file = easygui.fileopenbox("Choose image file",
                               "Open File",
                               filetypes=ALLOWED_FILE_EXT) # Issue: Dialog hides behind discord fullscreen
    _img = Image.open(file)
    img_array = np.array(_img, dtype=FILE_EXT_BIT[_img.format])
    img.image = _img
    img.base_image = img_array
    
if __name__ == '__main__':
    img = ImageObject()
    print(img.base_image)
    res = img.convert_array_to_img()
    res.show()
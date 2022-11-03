# Imports
from PIL import Image, ImageOps
import numpy as np
import attr

@attr.s(slots=True)
class ImageObject:
    image = attr.ib(default=None, type=Image)
    base_image = attr.ib(default=np.zeros((int(256/2), int(256/2)), dtype=np.int8), 
                   type=np.array)
    
    def convert_array_to_img(self):
        self.image = Image.fromarray(np.int8(self.base_image*255))
        return self.image
    
    
if __name__ == '__main__':
    img = ImageObject()
    print(img.base_image)
    res = img.convert_array_to_img()
    res.show()
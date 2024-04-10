from utils import slice_cubemap
from utils import cubemap_trim_floor
from py360convert import py360convert as py360

import subprocess
import numpy as np
from PIL import Image

def equi_to_cubemap(img_path, output_path):
    # read equi image
    img = np.array(Image.open(img_path))
    if len(img.shape) == 2:
        img = img[..., None]

    # convert image
    out = py360.e2c(img, 1520)

    # write cubemap image
    Image.fromarray(out.astype(np.uint8)).save(output_path)

def cut_floor_tile(img_path, output_path):
    # utils.slice_cubemap.slice_image(img_path, output_path)
    cubemap_trim_floor.slice_image(img_path, output_path)

if __name__ == '__main__':
    # TODO make img sizes dynamic for the whole process

    img_width = 0 # TODO
    img_height = 0 # TODO

    cubemap_square_width = 0 # TODO
    cubemap_square_row = 0 # TODO
    cubemap_square_height = 0 # TODO

    original_path = "shared-media/original.jpg"
    cubemap_path = "shared-media/cubemap.png"
    floortile_path = "shared-media/floortile.png"

    tripod_template_path = "" # TODO
    tripod_mask_path = "" # TODO

    # equi to cubemap
    equi_to_cubemap(original_path, cubemap_path)

    # cut out floor tile
    cut_floor_tile(cubemap_path, floortile_path)


from importlib import import_module
import sys
sys.path.append("Invariant-TemplateMatching")
sys.path.append("Inpaint-Anything")

template_matching = import_module('InvariantTM_rgbdiff')

from utils import cubemap_trim_floor
from utils import cubemap_glue_floor
from py360convert import py360convert as py360

import subprocess
import numpy as np
from PIL import Image

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def equi_to_cubemap(img_path, output_path):

    # read equi image
    img = np.array(Image.open(img_path))
    img_width = img.shape[0] // 2
    if len(img.shape) == 2:
        img = img[..., None]

    # convert image
    out = py360.e2c(img, img_width)

    # write cubemap image
    Image.fromarray(out.astype(np.uint8)).save(output_path)

def cubemap_to_equi(cubemap_path, original_path, output_path):
    # read cubemap image
    img = np.array(Image.open(cubemap_path))
    img_original = np.array(Image.open(original_path))
    img_width = img_original.shape[1]
    img_height = img_original.shape[0]
    out = py360.c2e(img, img_height, img_width)
    Image.fromarray(out.astype(np.uint8)).save(output_path)

def cut_floor_tile(img_path, output_path):
    # utils.slice_cubemap.slice_image(img_path, output_path)
    cubemap_trim_floor.slice_image(img_path, output_path)

def locate_tripod(floortile_path, tripod_template_path, tripod_mask_path):
    _, _, location = template_matching.InvariantTM_rgbdiff(floortile_path, tripod_template_path, tripod_mask_path)
    with open("shared-media/tripod_location.txt", "w") as file:
        file.write(f"{location[0]} {location[1]}")
    return location


if __name__ == '__main__':

    # ---------- RELATIVE PATHS SETTINGS ----------------------
    original_path = "shared-media/original.jpg"
    cubemap_path = "shared-media/cubemap.png"
    floortile_path = "shared-media/floortile.png"
    floortile_inpainted_path = "shared-media/inpainted_with_mask_2.png"
    cubemap_inpainted_path = "shared-media/cubemap_inpainted.png"
    final_equi_path = "shared-media/final.png"

    tripod_template_path = "shared-media/template/template_bg.jpg"
    tripod_mask_path = "shared-media/mask/mask_tripod.png"

    # ---------- TRIPOD REMOVAL WORKFLOW ----------------------

    # equi to cubemap
    logging.info("Convert equirectangular image to cubemap...")
    equi_to_cubemap(original_path, cubemap_path)

    # cut out floor tile
    logging.info("Cut out tile from cubemap...")
    cut_floor_tile(cubemap_path, floortile_path)

    # locate tripod
    logging.info("Locate tripod...")
    location = locate_tripod(floortile_path, tripod_template_path, tripod_mask_path)
    logging.info(f"Locating finished. Location: {location[0]} {location[1]}")

    # inpaint tripod
    logging.info("Inpaint tripod...")
    command = [
        "python", "Inpaint-Anything/remove_anything.py",
        "--input_img", floortile_path,
        "--coords_type", "key_in",
        "--point_coords", f"{location[0]}, {location[1]}",
        "--point_labels", "1",
        "--dilate_kernel_size", "15",
        "--output_dir", "../shared-media/inpainted/",
        "--sam_model_type", "vit_h",
        "--sam_ckpt", "sam_vit_h_4b8939.pth",
        "--lama_config", "lama/configs/prediction/default.yaml",
        "--lama_ckpt", "big-lama"
    ]

    try:
        subprocess.run(command)
    except Exception as e:
       logging.error("An error occurred:", exec_info=True)

    # insert inpainted floor into cubemap
    logging.info("Insert floor tile into cubemap...")
    cubemap_glue_floor.slice_image(cubemap_path, floortile_inpainted_path, cubemap_inpainted_path)

    # cubemap to equi
    logging.info("Convert inpainted cubemap to equirectangular image...")
    cubemap_to_equi(cubemap_inpainted_path, original_path, final_equi_path)





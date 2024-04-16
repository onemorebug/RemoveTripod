import cv2
import argparse


def slice_image(cubemap_path, floor_path, output_path):

    cubemap = cv2.imread(cubemap_path)
    floor_path = cv2.imread(floor_path)

    # get width / height of one cube
    cube_width = cubemap.shape[1] // 4

    cubemap[cube_width*2:cube_width*3,cube_width:cube_width*2] = floor_path

    cv2.imwrite(output_path, cubemap)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Paint white rectangle over image.")
    parser.add_argument("-o", "--output", help="Output filename", default="output_image.png")
    parser.add_argument("-c", "--cubemap", help="Cubemap filename", default="cubemap_template.png")
    parser.add_argument("-f", "--floor", help="Floor filename", default="cubemap_template.png")

    args = parser.parse_args()
    cubemap_filename = args.cubemap
    floor_filename = args.floor
    output_filename = args.output

    slice_image(cubemap_filename, floor_filename, output_filename)

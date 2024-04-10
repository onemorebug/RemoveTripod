import sys

import cv2
import argparse


def slice_image(input_path, output_path):

    cubemap = cv2.imread(input_path)

    trimmed_img = cubemap[3040:4560,1520:3040] # [y_from:y_to, x_from:x_to]

    cv2.imwrite(output_path, trimmed_img)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Paint white rectangle over image.")
    parser.add_argument("-o", "--output", help="Output filename", default="output_image.png")
    parser.add_argument("-i", "--input", help="Input filename", default="input_image.png")
    parser.add_argument("-height", "--height", help="Height of white rectangle from top", default=2600)

    args = parser.parse_args()
    output_filename = args.output
    input_filename = args.input
    rect_height = args.height

    slice_image(input_filename, output_filename, rect_height)


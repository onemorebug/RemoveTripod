import cv2
import argparse

def glue_images(input_path_top, input_path_bottom, output_path, glue_height):

    image_top = cv2.imread(input_path_top)
    image_bottom = cv2.imread(input_path_bottom)

    # +10: overlap 10 px so no gap is visible
    image_bottom[:glue_height+10,:] = image_top[:glue_height+10,:]

    cv2.imwrite(output_path, image_bottom)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Paint white rectangle over image.")
    parser.add_argument("-o", "--output", help="Output filename", default="output_image.png")
    parser.add_argument("-top", "--top", help="Filename top image", default="top.png")
    parser.add_argument("-bottom", "--bottom", help="Filename bottom image", default="bottom.png")
    parser.add_argument("-height", "--height", help="Glue height", default=2600)

    args = parser.parse_args()

    top_img_filename = args.top
    bottom_img_filename = args.bottom
    output_filename = args.output
    glue_height = args.height

    glue_images(top_img_filename, bottom_img_filename, output_filename, glue_height)

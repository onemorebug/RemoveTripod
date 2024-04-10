import cv2
import argparse


def slice_image(input_path, output_path, height):

    image = cv2.imread(input_path)

    rect_width = 6080
    rect_height = height

    cv2.rectangle(image, (0,0), (rect_width, rect_height), (255,255,255), thickness=cv2.FILLED)

    cv2.imwrite(output_path, image)

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



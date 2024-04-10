import cv2
import argparse


def slice_image(cubemap_path, floor_path, output_path):

    cubemap = cv2.imread(cubemap_path)
    floor_path = cv2.imread(floor_path)
    # trimmed_img = np.zeros((1520, 1520, 3), dtype=np.uint8)

    cubemap[3040:4560,1520:3040] = floor_path # [y_from:y_to, x_from:x_to]

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

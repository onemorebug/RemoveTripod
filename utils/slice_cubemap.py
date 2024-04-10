import cv2
import argparse
import os
# from py360convert import e2c
from py360convert import py360convert as e2c

def slice_image_folder(method, folder_path):
    cubemap_output_folder_name = "cubemaps"

    print("Folder! Path: ", folder_path)

    all_files = os.listdir(folder_path)

    image_extensions = ['.jpg', '.jpeg', '.png']

    image_files = [file for file in all_files if os.path.splitext(file)[-1].lower() in image_extensions]

    for image_file in image_files:
        print("Image: ", image_file)
        image_path = os.path.join(folder_path, image_file)
        image = cv2.imread(image_path)
        # TODO Refactor!!!
        if method == "slice":
            slice_image(image, image_file)
        elif method == "e2c":
            cubemap = e2c(image, face_w=1520)
            if not os.path.exists(f"img/{cubemap_output_folder_name}"):
                os.makedirs(f"img/{cubemap_output_folder_name}")
            cv2.imwrite(f"img/{cubemap_output_folder_name}/{image_file}", cubemap)


def slice_image(cubemap, image_name):

    # TODO make dynamic (function arguments)
    num_squares_x = 4
    num_squares_y = 3

    # define how the cubemap is structured
    cubemap_matrix = [[False, True, False, False], [True, True, True, True], [False, True, False, False]]

    cubemap_height = cubemap.shape[0]
    cubemap_width = cubemap.shape[1]

    cubemap_square_height = cubemap_height // num_squares_y
    cubemap_square_width = cubemap_width // num_squares_x

    # create folder for the image slices
    output_path = f"img/sliced/{image_name}/"
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for col in range(num_squares_y):
        for row in range(num_squares_x):
            if cubemap_matrix[col][row] is False:
                continue
            y_from = col * cubemap_square_height
            y_to = (col+1) * cubemap_square_height
            x_from = row * cubemap_square_width
            x_to = (row + 1) * cubemap_square_width

            cur_square = cubemap[int(y_from): int(y_to), int(x_from): int(x_to)]

            filename = f"img/sliced/{image_name}/sliced_col-{col}_row-{row}.png"
            cv2.imwrite(filename, cur_square)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Paint white rectangle over image.")
    parser.add_argument("-o", "--output", help="Output filename", default="output_image.png")
    parser.add_argument("-i", "--input", help="Input filename", default="input_image.png")
    parser.add_argument("-f", "--folder", help="Path to folder with images", default="")
    # TODO think about better way to integrate e2c in this application
    parser.add_argument("--e2c", help="e2c", action='store_true')

    args = parser.parse_args()
    output_filename = args.output
    input_filename = args.input
    folder_path = args.folder

    if folder_path != "" and folder_path is not None:
        if(args.e2c):
            print("Args: e2c!")
            slice_image_folder("e2c", folder_path)
        else:
            slice_image_folder("slice", folder_path)
    else:
        cubemap = cv2.imread(input_filename)
        slice_image(input_filename, output_filename)
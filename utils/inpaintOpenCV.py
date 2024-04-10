import cv2
import numpy as np

def remove_tripod():
    image = cv2.imread('img/cubemap-bilinear.png')
    mask = cv2.imread('masks/mask-detailed.png', 0)

    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # x1 = 3112
    # y1 = 703
    # x2 = 3454
    # y2 = 457
    #
    # cutout = image[y1:y2, x1:x2]
    #
    # inpaint = cv2.inpaint(image, cutout, inpaintRadius=3, flags=cv2.INPAINT_NS)

    inpaint = cv2.inpaint(image, mask, 1, cv2.INPAINT_NS)

    # scaling_factor = 0.3
    # inpaint = cv2.resize(inpaint, None, fx=scaling_factor, fy=scaling_factor)

    # cv2.imshow("inpainted", inpaint)
    cv2.imwrite("img/cubemap-inpaint.png", inpaint)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    remove_tripod()

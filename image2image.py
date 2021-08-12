"""
@author: Viet Nguyen <nhviet1009@gmail.com>
"""
import argparse
import cv2
import numpy as np
import glob
from itertools import product
import re

def get_args(output = "data/output.jpg"):
    parser = argparse.ArgumentParser("Viet Nguyen Photomosaic")
    parser.add_argument("--input", type=str, default="data/input.jpg", help="Path to input image")
    parser.add_argument("--output", type=str, default=output, help="Path to output image")
    parser.add_argument("--pool", type=str, default="tmp/avatars", help="Path to directory containing component images")
    parser.add_argument("--stride", type=int, default=30, help="size of each component image")
    args = parser.parse_args()
    return args


def get_component_images(path, size):
    images = []
    avg_colors = []
    images_path = []
    for image_path in glob.glob("{}/*.png".format(path)):
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        images.append(image)
        avg_colors.append(np.sum(np.sum(image, axis=0), axis=0) / (size ** 2))
        images_path.append(image_path)
    return images, np.array(avg_colors), images_path


def main(opt):
    images_usage = dict()

    input_image = cv2.imread(opt.input, cv2.IMREAD_COLOR)
    height, width, num_channels = input_image.shape
    blank_image = np.zeros((height, width, 3), np.uint8)
    images, avg_colors, images_path = get_component_images(opt.pool, opt.stride)
    for i, j in product(range(int(width / opt.stride)), range(int(height / opt.stride))):
        partial_input_image = input_image[j * opt.stride: (j + 1) * opt.stride,
                              i * opt.stride: (i + 1) * opt.stride, :]
        partial_avg_color = np.sum(np.sum(partial_input_image, axis=0), axis=0) / (opt.stride ** 2)
        distance_matrix = np.linalg.norm(partial_avg_color - avg_colors, axis=1)
        idx = np.argmin(distance_matrix)
        blank_image[j * opt.stride: (j + 1) * opt.stride, i * opt.stride: (i + 1) * opt.stride, :] = images[idx]

        result = re.search(r'tmp/avatars/([\w.-]+).png', images_path[idx])
        username = result.group(1)

        if username in images_usage:
            images_usage[username] += 1
        else:
            images_usage[username] = 1

    cv2.imwrite(opt.output, blank_image)
    return sorted(images_usage.items(), key=lambda item: item[1], reverse=True)


if __name__ == '__main__':
    opt = get_args()
    main(opt)
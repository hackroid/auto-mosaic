import cv2
import numpy as np


def im2single(im):
    im = im.astype(np.float32) / 255
    return im


def single2im(im):
    im *= 255
    im = im.astype(np.uint8)
    return im


def load_image(path):
    return im2single(cv2.imread(path))[:, :, ::-1]


def save_image(path, im):
    return cv2.imwrite(path, single2im(im.copy())[:, :, ::-1])


def im_range(im):
    im -= im.min()
    im = im / im.max()
    return im

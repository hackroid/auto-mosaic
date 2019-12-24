import requests
import json
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
from auth import *
from utils import *


def main(api_url, iam_auth_token_url):
    cutoff_frequency = 7
    filter = cv2.getGaussianKernel(ksize=cutoff_frequency*4+1, sigma=cutoff_frequency)
    filter = np.dot(filter, filter.T)
    token = get_token(iam_auth_token_url)
    img_path = './data/VOC2007test/JPEGImages/000069.jpg'
    files = {'images': open(img_path, 'rb')}
    headers = {'X-Auth-Token': token}
    r = requests.post(api_url, headers=headers, files=files)
    r_body = json.loads(r.text)
    detection_boxes = r_body['detection_boxes']
    detection_classes = r_body['detection_classes']
    detection_scores = r_body['detection_scores']
    img = load_image(img_path)
    for i, item in enumerate(detection_classes):
        if item == 'person':
            frame = detection_boxes[i]
            x1 = int(float(frame[0]))
            y1 = int(float(frame[1]))
            x2 = int(float(frame[2]))
            y2 = int(float(frame[3]))
            car = img[x1:x2, y1:y2]
            mosaic_car = cv2.filter2D(car, -1, filter)
            img[x1:x2, y1:y2] = mosaic_car
    plt.imshow(img)
    plt.show()


if __name__ == "__main__":
    iam_auth_url = 'https://iam.cn-north-4.myhuaweicloud.com/v3/auth/tokens'
    api_url_path = './data/iam/api_url'
    f = open(api_url_path, "r")
    api_url = f.read()
    f.close()
    main(api_url, iam_auth_url)

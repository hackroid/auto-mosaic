import requests
import json
import time
import math
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from auth import *
from utils import *

cutoff_frequency = 7
filterr = cv2.getGaussianKernel(ksize=cutoff_frequency*4+1, sigma=cutoff_frequency)
filterr = np.dot(filterr, filterr.T)

degree = 12
angle=45
M = cv2.getRotationMatrix2D((degree / 2, degree / 2), angle, 1)
motion_blur_kernel = np.diag(np.ones(degree))
motion_blur_kernel = cv2.warpAffine(motion_blur_kernel, M, (degree, degree))
motion_blur_kernel = motion_blur_kernel / degree


def single_img(api_url, iam_auth_token_url, img_path):
    token = get_token(iam_auth_token_url)
    print('===== func single_img =====')
    # img_path = './data/VOC2007test/JPEGImages/000069.jpg'
    print('>> loading img...')
    files = {'images': open(img_path, 'rb')}
    headers = {'X-Auth-Token': token}
    print('>> sending req')
    r = requests.post(api_url, headers=headers, files=files)
    r_body = json.loads(r.text)
    detection_boxes = r_body['detection_boxes']
    detection_classes = r_body['detection_classes']
    detection_scores = r_body['detection_scores']
    img = load_image(img_path)
    print('>> mosaic...')
    for i, item in enumerate(detection_classes):
        if item == 'person':
            frame = detection_boxes[i]
            x1 = abs(math.floor(float(frame[0])))
            y1 = abs(math.floor(float(frame[1])))
            x2 = abs(math.floor(float(frame[2])))
            y2 = abs(math.floor(float(frame[3])))
            car = img[x1:x2, y1:y2]
            mosaic_car = cv2.filter2D(car, -1, filterr)
            img[x1:x2, y1:y2] = mosaic_car
    print('>> mosaic done')
    print(detection_classes)
    return img


def video_proc(in_path, out_path, api_url, iam_auth_token_url):
    temp_path = './data/temp/tmp.jpg'
    video = cv2.VideoCapture(in_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    video_writer = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'MP4V'), fps, size)
    success, frame = video.read()
    index = 1
    while success:
        print("frame: {}/{}".format(str(index), str(frame_count)))
        save_image(temp_path, im2single(frame)[:,:,::-1])
        new_frame = single_img(api_url, iam_auth_token_url, temp_path)
        new_frame = single2im(new_frame)[:,:,::-1]
        print('>> writing back...')
        video_writer.write(new_frame)
        print('>> wrote')
        success, frame = video.read()
        # for i in range(5):
        #     if success:
        #         success, frame = video.read()
        #         index += 1
        index += 1
    video.release()


def main(api_url, iam_auth_token_url):
    img_path = './data/temp/tmp.jpg'
    in_path = './data/video/woman.mp4'
    out_path = './data/output/woman-mox.mp4'
    video_proc(in_path, out_path, api_url, iam_auth_token_url)
    img = single_img(api_url, iam_auth_token_url, img_path)
    plt.imshow(img)
    plt.show()



if __name__ == "__main__":
    iam_auth_url = 'https://iam.cn-north-4.myhuaweicloud.com/v3/auth/tokens'
    api_url_path = './data/iam/api_url'
    f = open(api_url_path, "r")
    api_url = f.read()
    f.close()
    main(api_url, iam_auth_url)

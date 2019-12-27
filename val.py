from auth import *
import os
import datetime as dt

ms = 0


def img_dan(api_url, iam_auth_token_url, img_path):
    """This func returns prediction of a single img

    Arguments:
        api_url {[str]} -- api url
        iam_auth_token_url {[str]} -- iam url
        img_path {[str]} -- path to img

    Returns:
        detection_boxes, detection_classes, detection_scores
    """
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
    return detection_boxes, detection_classes, detection_scores


def main():
    """ Calculating map of this test
    """

    iam_auth_url = 'https://iam.cn-north-4.myhuaweicloud.com/v3/auth/tokens'
    api_url_path = './data/iam/api_url'
    dataset_path = './data/test/JPEGImages/'
    # f = open(api_url_path, "r")
    # api_url = f.read()
    # f.close()
    iam_path = './data/iam/api_url'
    with open(api_url_path, 'r') as f:
        lines = f.readlines()
    api_links = [x.strip().split(' ') for x in lines]
    # api_links = api_links
    api_links[0] = api_links[0][0]
    api_links[1] = api_links[1][0]
    print(api_links)

    # img_path = './data/test/JPEGImages/000116.jpg'
    result = {
        'person': [],
        'car': [],
        'bird': [],
        'cat': [],
        'cow': [],
        'dog': [],
        'horse': [],
        'sheep': [],
        'aeroplane': [],
        'bicycle': [],
        'boat': [],
        'bus': [],
        'car': [],
        'motorbike': [],
        'train': [],
        'bottle': [],
        'chair': [],
        'diningtable': [],
        'pottedplant': [],
        'sofa': [],
        'tvmonitor': []
    }
    imagesetfile = './data/test/ImageSets/Layout/test.txt'
    imagesetpath = 'data/test/JPEGImages/{}.jpg'
    with open(imagesetfile, 'r') as f:
        lines = f.readlines()
    imagenames = [x.strip() for x in lines]
    print(len(imagenames))

    test_files = sorted(os.listdir(dataset_path))
    for test_f in imagenames:
        print(test_f)
        tmp = imagesetpath.format(test_f)
        if tmp.endswith('.jpg'):
            img_path = tmp
            detection_boxes, detection_classes, detection_scores = img_dan(
                api_links[ms], iam_auth_url, img_path)
            for i, item in enumerate(detection_classes):
                entry = [test_f.split(
                    '.')[0], detection_scores[i]] + detection_boxes[i]
                result[item].append(entry)
    # print(result)
    ct = dt.datetime.now()
    ct = format(ct).replace(' ', '').replace(
        '-', '').replace(':', '').replace('.', '')
    out_folder = './data/output/val/{}/'.format(ct)
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    for obj_class in iter(result):
        out_path = out_folder + 'comp3_det_test_{}.txt'.format(obj_class)
        f = open(out_path, "a")
        write_list = result[obj_class]
        for write_indi in write_list:
            luru = " ".join(write_indi).replace('-', '')
            f.write(luru)
            f.write('\n')
        f.close()


if __name__ == "__main__":
    main()

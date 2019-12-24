import datetime as dt
import requests
import json
import os


def req_token(ct, iam_auth_url):
    print('===== func req_token =====')
    token = None
    current_time = format(ct).replace(' ', '').replace(
        '-', '').replace(':', '').replace('.', '')
    print('>> Current time: {}'.format(format(ct)))

    auth_path = './data/iam/auth_data'
    f_name = "./data/iam/{}.aidate".format(current_time)

    f = open(auth_path, "r")
    body_data = f.read()
    body_data = json.dumps(json.loads(body_data))
    headers_data = {'Content-Type': 'application/json;charset=utf8'}
    f.close()

    print('>> Sending requests...')
    r = requests.post(url=iam_auth_url, headers=headers_data, data=body_data)
    print('>> Sending requests SUC')

    print('>> Getting token...')
    token = r.headers.get('X-Subject-Token')
    assert token != None
    print('>> Getting token SUC')

    print('>> Saving token {}'.format(f_name))
    f = open(f_name, "w+")
    f.write(token)
    f.close()
    print('>> Saving token SUC')
    return token


def get_token(iam_auth_token_url):
    print('===== func get_token =====')
    dayday = dt.timedelta(days=1) - dt.timedelta(hours=1)
    current_time = dt.datetime.now()
    token_path = './data/iam/'
    token = None

    files = os.listdir(token_path)
    if len(files) == 0:
        print('>> No file in token folder')
        token = req_token(current_time, iam_auth_token_url)
    else:
        print('>> Looking for valid token...')
        token_existence = False
        token_expire = True
        for f in files:
            if f.endswith('.aidate'):
                token_existence = True
                saved_token_time = f.split('.')[0]
                saved_token_time = dt.datetime.strptime(
                    saved_token_time,
                    '%Y%m%d%H%M%S%f'
                )
                if current_time - saved_token_time > dayday:
                    print('>> [DEL] expired token {}'.format(f))
                    os.remove(token_path + f)
                else:
                    token_expire = False
                    print('>> [READ] valid token {}'.format(f))
                    read_token = open(token_path + f, "r")
                    token = read_token.read()
        if not token_existence or token_expire:
            print('>> No valid token or all expired')
            token = req_token(current_time, iam_auth_token_url)
    return token

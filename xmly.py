#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
import json
import os
import time
import sys, getopt
import requests
import hashlib
import random

"""
参考来源：https://github.com/i-sync/ximalaya
"""


'''下载并写入文件'''
def down_file(file_name, url):
    if os.path.exists(file_name):
        os.remove(file_name)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }
    if url is None:
        return url
    res = requests.get(url, headers=headers)
    if res.status_code != requests.codes.ok:
        return None
    else:
        with open(file_name, 'wb') as f:
            f.write(res.content)



'''爬取喜马拉雅服务器系统时间戳，用于生成xm-sign'''
def getxmtime():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'Accept': 'text/html,application/xhtml+ xml,application/xml;q = 0.9,image/webp,image/apng,*/*;q=0.8, application/signe-exchange;v = b3',
        'Host': 'www.ximalaya.com'
    }
    url = "https://www.ximalaya.com/revision/time"
    response = requests.get(url, headers=headers)
    # print(response)
    return response.text


'''生成xm-sign'''
def getSign():
    """
    生成 xm-sign
    规则是 md5(himalaya-服务器时间戳)(100以内随机数)服务器时间戳(100以内随机数)现在时间戳
    :param serverTime:

    key: "getSign",
    value: function() {
        return function(t) {
            var e = Date.now();
            return "{himalaya-".concat(t, "}(").concat(c(100), ")").concat(t, "(").concat(c(100), ")").concat(e).replace(/{([\w-]+)}/, function(t, e) {
                return l(e)
            })
        }(s() ? Date.now() : window.XM_SERVER_CLOCK || 0)
    }
    :return:
    """
    serverTime = getxmtime()
    nowTime = str(round(time.time() * 1000))

    sign = str(hashlib.md5("himalaya-{}".format(serverTime).encode()).hexdigest()) + "({})".format(
        str(round(random.random() * 100))) + serverTime + "({})".format(str(round(random.random() * 100))) + nowTime
    print(sign)
    return sign


def album_list(album, order):
    json_name = os.path.dirname(__file__) + "/data/" + album + order + ".json"
    if os.path.exists(json_name):
        with open(json_name, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        return json_data

    all_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'Accept': 'text/html,application/xhtml+ xml,application/xml;q = 0.9,image/webp,image/apng,*/*;q=0.8, application/signe-exchange;v = b3',
        'Host': 'www.ximalaya.com'
    }

    index = 1
    while True:
        sign = getSign()
        # 加入xm-sign到header中
        headers['xm-sign'] = sign
        # 音频地址
        data_url = "https://www.ximalaya.com/revision/play/album?albumId={}&pageNum={}&sort={}&pageSize=30".format(album, index, order)
        print(data_url)
        res = requests.get(data_url, headers=headers)
        # return
        json_data = res.json()
        # print(py_dict)
        book_list = json_data['data']['tracksAudioPlay']
        all_list.extend(book_list)
        if not json_data['data']['hasMore']:
            break
        index = index + 1

    # save to file
    with open(os.path.dirname(__file__) + "/data/" + album + order + ".json", "w+", encoding="utf-8") as f:
        f.write(json.dumps(all_list, ensure_ascii=False))
    # return list
    return all_list


def get_argv(argv):
    try:
        opts, args = getopt.getopt(argv, "ha:o:p", ["help", "album=", "order=", "print"])
    except getopt.GetoptError:
        print('xmly.py -a <album id> -o <order 1 or -1> -p <only print list>')
        sys.exit(2)
    order = "1"
    p = False
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('xmly.py -a <album id> -o <order 1 or -1> -p <only print list>')
            sys.exit()
        elif opt in ("-a", "--album"):
            album = arg
        elif opt in ("-o", "--order"):
            order = arg
        elif opt in ("-p", "--print"):
            p = True
    return album, order, p


if __name__ == "__main__":
    album_id, order, p = get_argv(sys.argv[1:])
    base_path = "/home/miying2/xima"
    # base_path = "./files"
    for data in album_list(album_id, order):
        index = data["index"]
        track_name = data["trackName"]
        url = data["src"]
        album = data["albumName"]

        # remove default number from track_name
        # track_name = re.sub(r'\d+', '', track_name).strip()

        # print(name, url)
        file_path = base_path + "/" + album_id
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_name = "{}/{}_{}.m4a".format(file_path, index, track_name)
        print(file_name, url)

        # if p variable exist, so just print list name
        if p:
            continue

        # check file_name, if exists continue.
        if os.path.exists(file_name):
            print(file_name, "exists, skip...")
            continue
        down_file(file_name, url)
        # time.sleep(20)

    print("All Done.")
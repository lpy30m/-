# -*- coding: utf-8 -*-
"""
@author: 裴秀智Zz
@software: PyCharm
@file: ocr.py
@time: 2024-05-13 11:56
@Software: PyCharm
"""
import re
import time

import cv2
import execjs
import requests
from PIL import Image


def get_conf():
    url = "https://captcha.chaoxing.com/captcha/get/conf"
    params = {
        "callback": "jQuery1124025412723136620863_1715571059056",
        "captchaId": "npElQbBkROS2qozzS8V96ate7TBObVDF",
        "_": str(int(time.time()*1000))
    }
    response = requests.get(url, headers=headers, params=params)
    # print(response.text)
    t = re.findall('"t":(.*?),',response.text)[0]
    print(t)
    return t


def identify_gap(bg, tp, out):
    '''
    bg: 背景图片
    tp: 缺口图片
    out:输出图片
    '''
    # 读取背景图片和缺口图片
    bg_img = cv2.imread(bg)  # 背景图片
    tp_img = cv2.imread(tp)  # 缺口图片

    # 识别图片边缘
    bg_edge = cv2.Canny(bg_img, 100, 200)
    tp_edge = cv2.Canny(tp_img, 100, 200)

    # 转换图片格式
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)

    # 缺口匹配
    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配

    # 绘制方框
    th, tw = tp_pic.shape[:2]
    tl = max_loc  # 左上角点的坐标
    br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
    cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
    cv2.imwrite(out, bg_img)  # 保存在本地

    # 返回缺口的X坐标
    return tl[0]

def get_img():
    url = "https://captcha.chaoxing.com/captcha/get/verification/image"
    captchaKey = execjs.compile(open('./1.js', 'r', encoding="utf-8").read()).call('getcaptchaKey',t)
    token = execjs.compile(open('./1.js', 'r', encoding="utf-8").read()).call('gettoken',t,captchaId,captchaKey)
    params = {
        "callback": "jQuery1124025412723136620863_1715571059056",
        "captchaId": captchaId,
        "type": "slide",
        "version": "1.1.16",
        "captchaKey": captchaKey,
        "token": token,
        "referer": "https://user.dayainfo.com/show/login",
        "_": str(int(time.time()*1000))
    }
    response = requests.get(url, headers=headers, params=params)
    print(response.text)
    tk = re.findall('"token":"(.*?)"',response.text)[0]
    bgImgUrl = re.findall('"shadeImage":"(.*?)"',response.text)[0]
    puzzleImgUrl = re.findall('"cutoutImage":"(.*?)"',response.text)[0]
    bg = requests.get(bgImgUrl, headers=headers)
    with open('bg.png', 'wb') as w:
        w.write(bg.content)
    img = Image.open('bg.png')
    out = img.resize((320, 168), Image.LANCZOS)
    out.save('new_bg.png')
    fg = requests.get(puzzleImgUrl, headers=headers)
    with open('fg.png', 'wb') as w:
        w.write(fg.content)
    img = Image.open('fg.png')
    out = img.resize((56, 160), Image.LANCZOS)
    out.save('new_fg.png')
    distance = identify_gap('new_bg.png', 'new_fg.png', "1.png")
    print(distance)
    return tk,distance

def verify():
    url = "https://captcha.chaoxing.com/captcha/check/verification/result"
    params = {
        "callback": "jQuery1124025412723136620863_1715571059056",
        "captchaId": captchaId,
        "type": "slide",
        "token": tk,
        "textClickArr": "[{\"x\":145}]",
        "coordinate": "[]",
        "runEnv": "10",
        "version": "1.1.16",
        "_": str(int(time.time()*1000))
    }
    new_text_click_arr = '[{"x":' + str(distance) + '}]'
    params["textClickArr"] = new_text_click_arr
    print(params)
    response = requests.get(url, headers=headers, params=params)
    print(response.text)


if __name__ == '__main__':
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Referer": "https://user.dayainfo.com/",
        "Sec-Fetch-Dest": "script",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
        "sec-ch-ua": "\"Chromium\";v=\"124\", \"Microsoft Edge\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    t = get_conf()
    captchaId = "npElQbBkROS2qozzS8V96ate7TBObVDF"
    tk,distance = get_img()
    verify()
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

# 定制请求头
headers = {'Referer':'https://www.mzitu.com','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3679.0 Safari/537.36'}

path = 'R:/python123全国等考/meizitu/'
meizi_url = []
meizitu_img = []

start_url = 'https://www.mzitu.com/177007'
meizi_url.append(start_url)
r = requests.get(start_url)
soup = BeautifulSoup(r.text)
main_img = soup.find('div', 'main-image').img.get('src')
meizitu_img.append(main_img)

guess_like = soup.find('dl', 'widgets_like').find_all('a')
for a in guess_like:
    meizi_url.append(a.get('href'))
# 删除起始引导url
# del meizi_url[0]

# print(meizi_url)
# print(meizitu_img)
with open("R:/python123全国等考/meizitu/meizi-main-jpg.txt", "w") as fo:
    x = 1
    y = 1
    for node_url in meizi_url:
        r = requests.get(node_url)
        soup = BeautifulSoup(r.text)
        main_img = soup.find('div', 'main-image').img.get('src')
        # 添加到文件日志并下载主图
        if main_img not in meizitu_img:
            x += 1
            meizitu_img.append(main_img)
            # 写入日志
            fo.write(main_img+'\n')
            # 下载主图
            res = requests.get(main_img, headers=headers)
            if res.status_code == 200:
                with open(path+str(x)+'-'+str(y)+'.jpg', 'wb') as f:
                    f.write(res.content)
                    print('成功保存图片')  
        # 猜你喜欢，跳转其他页面
        guess_like = soup.find('dl', 'widgets_like').find_all('a')
        for a in guess_like:
            like = a.get('href')
            # 添加推荐页面
            if like not in meizi_url:
                y += 1
                meizi_url.append(like)



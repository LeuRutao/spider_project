# _*_ coding: utf-8 _*_
import time

__author__ = 'Leurutao'
__date__ = '2019/5/30 15:59'

import requests
from pymongo import MongoClient

client = MongoClient()
db = client.lagou
lagou = db.jobs_pachong

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Referer': 'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=',
}
def get_job_infos(page, kd):
    for i in range(page):
        payload = {
            'first': 'false',
            'pn': i,
            'kd': kd,
        }
        url_parse = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
        url_start = 'https://www.lagou.com/jobs/list_?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput='
        s = requests.Session()
        s.get(url_start, headers=headers, timeout=3) #请求首页获取cookies
        cookie = s.cookies # 为此次获取的cookies
        # print(cookie)
        response = s.post(url_parse, data=payload, headers = headers, cookies = cookie, timeout=3)
        # print(response.request.headers)
        if 'content' in list(response.json().keys()):
            print("yes")
            job_json = response.json()['content']['positionResult']['result']

            lagou.insert_many(job_json)

            print('正在爬取第' + str(i + 1) + '页的数据...')
            time.sleep(2)
        else:
            print("no")

if __name__ == '__main__':
    get_job_infos(20, '爬虫')
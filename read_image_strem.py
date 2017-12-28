#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/20 19:49
# @Author  : youqingkui
# @File    : read_image_strem.py
# @Desc    :
import pickle
import time
import requests
from celery_app.s3_up import put_image_s3
from celery_app.task1 import add

r = requests.get('http://192.168.31.190:8080/video', stream=True)
if(r.status_code == 200):
    data = b''
    for chunk in r.iter_content(1024):
        data += chunk
        jpg_start = data.find(b'\xff\xd8')
        jpg_end = data.find(b'\xff\xd9')
        if jpg_start != -1 and jpg_end != -1:
            jpg = data[jpg_start:jpg_end + 2]
            data = data[jpg_end + 2:]
            current_time = time.time()
            image_name = '%s.jpg' % (current_time)
            params = {'image_name':image_name, 'content':pickle.dumps(jpg)}
            # put_image_s3.delay(params)
            put_image_s3.apply_async((params,), serializer='pickle')
else:
    print("Received unexpected status code {}".format(r.status_code))

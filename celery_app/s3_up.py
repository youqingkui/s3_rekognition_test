#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/20 19:42
# @Author  : youqingkui
# @File    : s3_up.py
# @Desc    :

import pickle
import boto3
from celery_app import app


s3 = boto3.resource('s3')

@app.task()
def put_image_s3(data_info):
    image_name = data_info.get('image_name')
    content = data_info.get('content')
    res = s3.Bucket('s3-youqingkui').put_object(Key=image_name, Body=pickle.loads(content))
    print(res)



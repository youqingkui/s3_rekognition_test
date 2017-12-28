#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/21 14:47
# @Author  : youqingkui
# @File    : task2.py
# @Desc    :


import time
from celery_app import app

@app.task
def multiply(x, y):
    time.sleep(2)
    return x * y
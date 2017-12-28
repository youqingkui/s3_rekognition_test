#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/21 14:45
# @Author  : youqingkui
# @File    : __init__.py.py
# @Desc    :

from celery import Celery

app = Celery('demo')
app.config_from_object('celery_app.celeryconfig')

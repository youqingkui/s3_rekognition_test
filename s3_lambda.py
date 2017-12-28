#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/28 10:53
# @Author  : youqingkui
# @File    : s3_lambda.py
# @Desc    :


import boto3
import urllib
from PIL import Image
import io


rekognition = boto3.client('rekognition', 'us-west-2')
s3 = boto3.client('s3')


def detect_faces(bucket, key):
    response = rekognition.detect_faces(Image={"S3Object": {"Bucket": bucket, "Name": key}})
    return response


def lambda_handler(event, context):
    # bucket = event['Records'][0]['s3']['bucket']['name']
    # key = urllib.parse.quote(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    bucket = 'yk-rekognition'
    key = 'drive_resized.jpg'
    key = 'IMG_0007.jpg'
    try:
        response = detect_faces(bucket, key)
        FaceDetails = response.get('FaceDetails', [])
        if not FaceDetails:
            print("not find FaceDetails => %s" % response)

        for face in FaceDetails:
            BoundingBox = face.get('BoundingBox', {})
            image_data = s3.get_object(Bucket=bucket, Key=key)['Body'].read()
            image = Image.open(io.BytesIO(image_data))

            left = image.width * BoundingBox['Left']
            top = image.height * BoundingBox['Top']
            width = left + (image.width * BoundingBox['Width'])
            height = top + (image.height * BoundingBox['Height'])
            region = (left, top, width, height)
            print(region)
            face_image = image.crop(region)
            face_image.show()
        print(response)

        return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e

if __name__ == '__main__':
    lambda_handler(123, 321)
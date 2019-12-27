# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 16:14:52 2019

@author: julien
"""
import requests
import settings.settings as settings
from log import Logger
import time
import json

logger = Logger(__name__).run()

def uploadImageRealTime(Q):
    while True:
        cam, result , img = Q.get()
        logger.info('get image from queue real on cam  : {}'.format(cam))
        files = {'myFile': img}
        imgJson = {'key': settings.KEY, 'img_name': 'temp_img_cam_'+cam+'.jpg', 'result' : json.dumps(result)}
    try :
        requests.post(settings.SERVER+"uploadimage", files=files, data = imgJson)
    except requests.exceptions.ConnectionError :
        logger.warning('uploadImageRealTime Can not find the remote server')
        pass
    logger.warning('send json image real : {}'.format(imgJson))



def uploadImage(Q):
    server = True
    while True:
        if server :
            img = Q.get()
            logger.info('get image from queue : {}'.format(img[0]))
            files = {'myFile': img[1]}
            imgJson = {'key': settings.KEY, 'img_name': img[0]}
        try :
            requests.post(settings.SERVER+"uploadimage", files=files, data = imgJson)
            server = True
        except requests.exceptions.ConnectionError :
            server = False
            logger.warning('getState Can not find the remote server')
            pass
        logger.warning('send json : {}'.format(imgJson))

def uploadResult(Q):
    server = True
    while True:
        if server :
            logger.warning('starting upload result')
            result = Q.get()
            logger.info('get result from queue : {}'.format(result))
            img, cam,  result_filtered, result_darknet = result[0], result[1], [(r[0].decode(),r[1],r[2]) for r in result[2] ], [(r[0].decode(),r[1],r[2]) for r in result[3] ]
            resultJson = {'key': settings.KEY, 'img' : img, 'cam' : cam, 'result_filtered' : result_filtered, 'result_darknet' : result_darknet }
        try :
            requests.post(settings.SERVER+"uploadresult", json=resultJson)
        except requests.exceptions.ConnectionError :
            server = False
            logger.warning('getState Can not find the remote server')
            pass
        logger.warning('send json : {}'.format(resultJson))
        

def getState(E):
    while True:
        try :
            r = requests.post(settings.SERVER+"getState", data = {'key': settings.KEY, } )
            rec = json.loads(r.text)[0]['rec']
            if rec :
                E.set()
            else :
                E.clear()
        except requests.exceptions.ConnectionError :
            logger.info('getState Can not find the remote server')
            time.sleep(5)
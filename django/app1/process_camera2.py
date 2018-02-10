# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 11:58:19 2018

@author: julien

Main script to process the camera images
"""
import logging
import requests
import os
import sys
import cv2

from threading import Thread, Lock, Event
from logging.handlers import RotatingFileHandler
from scipy.misc import imread
from io import BytesIO
from django.core.files import File

#------------------------------------------------------------------------------
# a simple config to create a file log - change the level to warning in
# production
#------------------------------------------------------------------------------
level= logging.INFO
logger = logging.getLogger()
logger.setLevel(level)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler('camera.log', 'a', 10000000, 1)
file_handler.setLevel(level)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(level)
logger.addHandler(stream_handler)

#------------------------------------------------------------------------------
# Because this script have to be run in a separate process from manage.py
# you need to set up a Django environnement to use the Class defined in
# the Django models. It is necesssary to interact witht the Django database
#------------------------------------------------------------------------------
# to get the projet.settings it is necessary to add the parent directory
# to the python path
try:
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
except NameError:
    sys.path.append(os.path.abspath('..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projet.settings")
import django
django.setup()

from app1.models import Camera, Result, Object
from app1.darknet_python import darknet as dn
#------------------------------------------------------------------------------

# locking process to avoid threads calling darknet more than once at a time
lock = Lock()

# the base condition to store the image is : is there a new objects detection
# or a change in the localisation of the objects. It is not necessary to store
# billions of images but only the different one.



class ProcessCamera(Thread):
    """Thread used to grab camera images and process the image with darknet"""
    def __init__(self, cam, event_list, nb_cam):
        Thread.__init__(self)
        self.cam = cam
        self.event_list = event_list
        self.cam_id = cam.id-1
        self.nb_cam = nb_cam
        self.running = False
        self.result_DB = []
 
    def run(self):
        """code run when the thread is started"""
        self.running = True
        while self.running :
            r = requests.get(self.cam.url, auth=(self.cam.username,
                                                 self.cam.password
                                                 ), stream=True)
            if r.status_code == 200 :
                img_bytes = BytesIO(r.content)
                arr = imread(img_bytes)
                im = dn.array_to_image(arr)
                logger.debug('image ready for darknet :  {} '.format(im))
                self.event_list[self.cam_id].wait()
                logger.debug('cam {} alive'.format(self.cam_id))
                with lock:
                   result_darknet = dn.detect2(net, meta, im,thresh=0.5)
                   logger.info('get result from darknet : {}\n'.format(
                   result_darknet))             
                # compare with last result to check if different
                if base_condition(self.result_DB,result_darknet):
                    logger.debug('>>> Result have changed <<< ')             
                    result_DB = Result(camera=self.cam)
                    # il faut utiliser opencv pour faire les box
                    result_DB.file.save('detect',File(img_bytes))
                    result_DB.save()
                    for r in result_darknet:
                        object_DB = Object(result = result_DB, 
                                           result_object=r[0],
                                           result_prob=r[1],
                                           result_loc1=r[2][0],
                                           result_loc2=r[2][1],
                                           result_loc3=r[2][2],
                                           result_loc4=r[2][3])
                        object_DB.save()
                    logger.info('--------- Result store in DB -------------\n')
                    self.result_DB = result_darknet
            
            else:
                logger.warning('bad camera download on {} \n'
                             .format(self.cam.name))
            self.event_list[((self.cam_id)+1)%self.nb_cam].set()
            logger.debug('cam {} set'.format((self.cam_id+1)%self.nb_cam))
            self.event_list[self.cam_id].clear()
            
        
    def base_condition(self,new):
    sensivity = 40
    threshold = 0.6
    # are the detected objects the same
    new_thresh = [i for i in new if r[1]>threshold]
    if [r[0] for r in new_tresh] == [r[0] for r in self.result_DB]:
        #objects are same use map(none,a,b) on list.sort() puis egal ou >tresh
    
    

        if abs(sum([i-j for i,j in zip(
        [i for j in old for i in j[2]], [i for j in new for i in j[2]])])
        )>sensivity*len(new):
            logger.info('New position detected - change of : {}'.format(abs(
            sum([i-j for i,j in zip([i for j in old for i in j[2]],
                                    [i for j in new for i in j[2]])]))))
            self.result_DB = new_tresh            
            return True
        else:
            return False
        
    
    if not ([i[0] for i in old if r[1]>threshold]  ==
    [i[0] for i in new if r[1]>threshold] ):
        logger.info('Change in detected objects : {}'.format(set([i[0]
        for i in old])^set([i[0] for i in new]))):
        # it is important to check if the object have
        return True
    # are the location different 
    # modifier la sensibilité selon le nb d'objets
    
    return False
                
# get all the cameras in the DB
cameras = Camera.objects.all()
nb_cam = len(cameras)

# create one event for each camera. So the thread will be able to communicate
# between each other using this event. It is necesary to tell other threads
# when the darknet process is over. 
event_list = [Event() for _ in range(nb_cam)]

# create one thread per camera
thread_list = [ ProcessCamera(c,event_list, nb_cam) for c in cameras]

# load the Neural Network and the meta
net = dn.load_net(b"darknet_python/cfg/yolo.cfg", b"../../yolo.weights", 0)
meta = dn.load_meta(b"darknet_python/cfg/coco.data")
   
def main():
    for t in thread_list:
        t.start()
    thread_list[0].event_list[0].set()
    
def stop():
    for t in thread_list:
        t.running=False

# start the threads
if __name__ == 'main':
    # grzet
    pass

# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 11:58:19 2018

@author: julien

Main script to process the camera images
"""
import logging
import time
import requests
import os
import sys
import cv2
from django.conf import settings
from threading import Thread, Lock, Event
from logging.handlers import RotatingFileHandler
from io import BytesIO
from django.core.files import File
from django.db import transaction


#------------------------------------------------------------------------------
# Because this script have to be run in a separate process from manage.py
# you need to set up a Django environnement to use the Class defined in
# the Django models. It is necesssary to interact witht the Django database
#------------------------------------------------------------------------------
# to get the projet.settings it is necessary to add the parent directory
# to the python path
try:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
except NameError:
    sys.path.append(os.path.abspath('..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projet.settings")
import django
django.setup()

#------------------------------------------------------------------------------
# a simple config to create a file log - change the level to warning in
# production
#------------------------------------------------------------------------------
if settings.DEBUG : 
    level=logging.DEBUG
else:
    level=logging.WARNING
logger = logging.getLogger()
logger.setLevel(level)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler(os.path.join(settings.BASE_DIR,'camera.log'), 'a', 10000000, 1)
file_handler.setLevel(level)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
#stream_handler = logging.StreamHandler()
#stream_handler.setLevel(level)
#logger.addHandler(stream_handler)

#------------------------------------------------------------------------------

from app1.models import Camera, Result, Object
from app1.darknet_python import darknet as dn



# function to extract same objects in 2 lists
def get_list_same (l_old,l_under,thresh):
    l_old_w = l_old[:]
    new_element = []
    for e_under in l_under :
        for e_old in l_old_w:
            if e_under[0]==e_old[0] :
                diff_pos = (sum([abs(i-j) for i,j in zip(e_under[2],e_old[2])]))
                if diff_pos < thresh :
                    new_element.append(e_old)
                    l_old_w.remove(e_old)
    return new_element

def get_list_diff(l_new,l_old,thresh):
    new_copy = l_new[:]
    old_copy = l_old[:]
    for e_new  in  l_new:
        flag = False
        limit_pos = thresh
        for e_old in l_old:
            if e_new[0]==e_old[0] :
                diff_pos = (sum([abs(i-j) for i,j in zip(e_new[2],e_old[2])]))
                if diff_pos < thresh :
                    flag = True
                    if diff_pos < limit_pos:
                        limit_pos = diff_pos
                        to_remove = (e_new,e_old)            
        if flag:
            new_copy.remove(to_remove[0])
            old_copy.remove(to_remove[1])
    return new_copy,old_copy

def read_write(rw,*args):
    if rw=='r':
        im = cv2.imread(*args)
        return im
    if rw=='w':
        r = cv2.imwrite(*args)
        return r


# the base condition to store the image is : is there a new objects detection
# or a change in the localisation of the objects. It is not necessary to store
# billions of images but only the different one.

class ProcessCamera(Thread):
    """Thread used to grab camera images and process the image with darknet"""
    def __init__(self, cam, event_ind):
        Thread.__init__(self)
        self.cam = cam
        self.event_ind = event_ind
        self.running = False
        self.running_rtsp = False
        self.img_temp = os.path.join(settings.MEDIA_ROOT,'tempimg_cam'+str(self.cam.id)+'.jpg')
        self.img_temp_box = os.path.join(settings.MEDIA_ROOT,'tempimg_cam'+str(self.cam.id)+'_box.jpg')
        self.pos_sensivity = cam.pos_sensivity
        self.request_OK = False
        self.black_list=(b'pottedplant',b'cell phone')
        #self.black_list=()
        self.clone={b'cell phone':b'car'}
        ###  getting last object in db for camera to avoid writing same images at each restart
        r_last = Result.objects.filter(camera=cam).last()
        if r_last :
            o_last = Object.objects.filter(result_id=r_last.id)
            result_last = [(r.result_object.encode(), float(r.result_prob),
                            (float(r.result_loc1),float(r.result_loc2),
                             float(r.result_loc3),float(r.result_loc4))) for r in o_last]
            self.result_DB = result_last
        else :
            self.result_DB = []
        if cam.auth_type == 'B':
            self.auth = requests.auth.HTTPBasicAuth(cam.username,cam.password)
        if cam.auth_type == 'D' :
            self.auth = requests.auth.HTTPDigestAuth(cam.username,cam.password)
        
        self.lock = Lock()
    
    def grab(self):
        self.vcap = cv2.VideoCapture(self.cam.rtsp)
        i=15
        j=0
        while self.running_rtsp :
            if i==15:
                date = time.strftime("%Y-%m-%d-%H-%M-%S")
                ret, frame = self.vcap.read()
                self.running_rtsp = ret
                logger.debug("resultat de la lecture {} rtsp : {} ".format(j,ret))
                logger.debug('*** {}'.format(date))
                t = time.time()
                if ret and len(frame)>100 :
                    if self.cam.reso:
                        if frame.shape[0]!=self.cam.height or frame.shape[1]!=self.cam.width:
                            frame = cv2.resize(frame,(self.cam.width, self.cam.height), interpolation = cv2.INTER_CUBIC)
                    with self.lock:
                        self.request_OK = read_write('w',self.img_temp, frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
                    logger.debug("resultat de l'ecriture du fichier jpg : {} en {} ".format(
                            self.request_OK,time.time()-t))
                i=0
            i+=1
            j+=1
            self.vcap.grab()


    def run(self):
        """code run when the thread is started"""
        self.running = True
        while self.running :
            t=time.time()
            
            
            # Special stop point for dahua nvcr which can not answer multiple fast http requests
            if not threated_requests :
                event_list[self.event_ind].wait()
                logger.debug('cam {} alive'.format(self.cam.id))
            #-----------------------------------------------------------------------------------
            
            
            #******************************Grab images in http ********************************
            if not self.cam.stream :
                self.request_OK = True
                try :
                    r = requests.get(self.cam.url, auth=self.auth, stream=False, timeout=4)
                    if r.status_code == 200 and len(r.content)>1000 :
                        with open(self.img_temp, 'wb') as fd:
                            #for chunk in r.iter_content(chunk_size=128):
                             fd.write(r.content)
                        logger.info('image saved to temp folder for darknet in {}s '.format(
                                     time.time()-t))
                    else:
                        self.request_OK = False
                        logger.warning('bad camera download on {} \n'.format(self.cam.name))    
                except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                    self.request_OK = False
                    logger.warning('network error on {} \n'.format(self.cam.name))
                    pass
                
            #*****************************Grab image in rtsp **********************************
            else :
                if not self.running_rtsp:
                    logger.info('rtsp not running, so launch '.format(
                                     time.time()-t))
                    self.running_rtsp = True
                    _thread = Thread(target=self.grab)
                    _thread.start()
            #*************************************************************************************    
            t=time.time()
            # Normal stop point for ip camera-------------------------------
            if threated_requests :
                event_list[self.event_ind].wait()
                logger.debug('cam {} alive'.format(self.cam.id))
            #---------------------------------------------------------------
            if self.request_OK:
                
                with self.lock:
                    arr = read_write('r',self.img_temp)   
                    th = self.cam.threshold*(1-(float(self.cam.gap)/100))
                    result_darknet = dn.detect(net, meta, self.img_temp.encode(),
                                               thresh=th,
                                               hier_thresh = 0.4)
                logger.debug('thresh set to {}'.format(th))
                logger.info('get brut result from darknet : {} in {}s\n'.format(
                result_darknet,time.time()-t))
                event_list[self.event_ind].clear()
                logger.debug('cam {} clear -> so wait !'.format(self.cam.id))
                event_list[((self.event_ind)+1)%nb_cam].set()
                logger.debug('event {} set'.format((self.event_ind+1)%nb_cam))

                # get only result above trheshlod or previously valid
                t=time.time()
                result_filtered = self.check_thresh(result_darknet)
                # compare with last result to check if different
                arrb = arr.copy()
                for r in result_filtered:
                    box = ((int(r[2][0]-(r[2][2]/2)),int(r[2][1]-(r[2][3]/2
                    ))),(int(r[2][0]+(r[2][2]/2)),int(r[2][1]+(r[2][3]/2
                    ))))
                    cv2.rectangle(arrb,box[0],box[1],(0,255,0),3)
                    cv2.putText(arrb,r[0].decode(),box[1],
                    cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2)
                cv2.imwrite(self.img_temp_box,arrb)
                if self.base_condition(result_filtered) and Camera.objects.get(id=
                                      self.cam.id).rec:
                    logger.debug('>>> Result have changed <<< ')
                    with transaction.atomic():
        		           result_DB = Result(camera=self.cam,brut=result_darknet)
        		           date = time.strftime("%Y-%m-%d-%H-%M-%S")
        		           img_bytes = BytesIO(cv2.imencode('.jpg', arr)[1].tobytes())
        		           result_DB.file1.save('detect_'+date+'.jpg',File(img_bytes)) 
        		           for r in result_filtered:
        		               object_DB = Object(result = result_DB, 
        		                                  result_object=r[0].decode(),
        		                                  result_prob=r[1],
        		                                  result_loc1=r[2][0],
        		                                  result_loc2=r[2][1],
        		                                  result_loc3=r[2][2],
        		                                  result_loc4=r[2][3])
        		               object_DB.save()
        		           img_bytes_rect = BytesIO(cv2.imencode('.jpg', arrb)[1].tobytes())
        		           result_DB.file2.save('detect_box_'+date+'.jpg',File(img_bytes_rect))
        		           result_DB.save()
                    logger.info('>>>>>>>>>>>>>>>--------- Result store in DB '
                    '-------------<<<<<<<<<<<<<<<<<<<<<\n')
                    self.result_DB = result_filtered    
                logger.info('brut result process in {}s '.format(time.time()-t))
            else :
                event_list[self.event_ind].clear()
                logger.debug('cam {} clear -> so wait !'.format(self.cam.id))
                event_list[((self.event_ind)+1)%nb_cam].set()
                logger.debug('event {} set'.format((self.event_ind+1)%nb_cam))
                time.sleep(0.5)

    def base_condition(self,new):
        compare = get_list_diff(new,self.result_DB,self.pos_sensivity)
        if len(compare[0])==0 and len(compare[1])==0 :
            return False
        else:
            logger.info('Change in objects detected : new={} lost={}'
            .format(compare[0], compare[1]))
            return True

    def check_thresh(self,resultb):
        result = [r for r in resultb if r[0] not in self.black_list]
        #result = [(e1,e2,e3) if e1 not in self.clone else (self.clone[e1],e2,e3)
        #for (e1,e2,e3) in result]
        rp = [r for r in result if r[1]>=self.cam.threshold]
        rm = [r for r in result if r[1]<self.cam.threshold]
        if len(rm)>0:
            rs = get_list_same(self.result_DB,rp,self.pos_sensivity)
            ro = [item for item in self.result_DB if item not in rs]
            diff_objects = get_list_same(ro,rm,self.pos_sensivity)
            logger.debug('objects from last detection now under treshold :{} '
            .format(diff_objects))
            rp+=diff_objects
        logger.debug('the filtered list of detected objects is {}'.format(rp))
        return rp

# get all the cameras in the DB
cameras = Camera.objects.filter(active=True)
nb_cam = len(cameras)

# choose if you want to download the image in parallel thread. 
threated_requests = settings.THREATED_REQUESTS

# create one event and one thread for each camera. So the thread will be able to communicate
# between each other using this event. It is necesary to tell other threads
# when the darknet process is over. 
thread_list = []
event_list = []
for c in cameras:
    event_list.append(Event())
    thread_list.append(ProcessCamera(c,len(event_list)-1))



# load the Neural Network and the meta
path = settings.DARKNET_PATH
cfg = os.path.join(path,settings.CFG).encode()
weights = os.path.join(path,settings.WEIGHTS).encode()
data = os.path.join(path,settings.DATA).encode()

net = dn.load_net(cfg,weights, 0)
meta = dn.load_meta(data)

def main():
    for t in thread_list:
        t.start()
    event_list[0].set()
    print('darknet is running...')
    # Just run4ever (until Ctrl-c...)
    try:
        while(True):
            time.sleep(1000)
    except KeyboardInterrupt:
        print("Bye bye!")

def stop():
    for t in thread_list:
        t.running=False

def start():
    for t in thread_list:
        t.running=True

# start the threads
if __name__ == '__main__':
    main()



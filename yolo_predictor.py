import sys, os
import cv2
from ctypes import *
import numpy as np
from skimage import io
import requests
import datetime


sys.path.append(os.path.join(os.getcwd(), 'darknet/python/'))
from darknet import *


class Yolo_predictor:

    def __init__(self, preffix):
        # prepare model for usage
        self.cfg, self.weights, metap = self.prepare_all_paths(preffix, "cfg/yolov3.cfg", "yolov3.weights", "cfg/coco.data")
        self.meta = load_meta(metap)
        self.net = load_net(self.cfg, self.weights, 0)

    def prepare_all_paths(self, path_to_darknet, path_to_cfg, path_to_weights, path_to_meta):
        prefix = path_to_darknet.encode('ascii')

        cfg_path = prefix + path_to_cfg.encode('ascii')
        weights_path = prefix + path_to_weights.encode('ascii')
        meta_path = prefix + path_to_meta.encode('ascii')

        return (cfg_path, weights_path, meta_path)
    
    
    def preprocess_coords(self, coords):
        # since coordintes from yolo defferent from cv2 we need to transform it
        
        width = coords[2]
        height = coords[3]
        center_x = coords[0]
        center_y = coords[1]

        bottomLeft_x = center_x - (width / 2)
        bottomLeft_y = center_y - (height / 2)

        topRight_x = bottomLeft_x + width
        topRight_y = bottomLeft_y + height

        point1 = (int(bottomLeft_x), int(bottomLeft_y))
        point2 = (int(topRight_x), int(topRight_y))
        point3 = (int(bottomLeft_x), int(bottomLeft_y) - 5)

        return (point1, point2, point3)

    def get_image_path(self, update):
    
        # getting message from update
        message = update.message
        img_path = None
        
        # attenpt to get photo from message and save it on server
        if message.photo != None:
            photo_file = message.bot.get_file(message.photo[2].file_id)
            responce = requests.get(img_telegram_object.file_path)
            img_path = os.path.join(os.getcwd(), 'imgs', img_telegram_object.file_id)
            
            with open(img_path, 'wb') as f:
                f.write(responce.content)
            f.close()
            
        return img_path



    def process(self, update):
    
        # color & font for bounding boxes and names
        color = (177, 33, 211)
        font = cv2.FONT_HERSHEY_SIMPLEX

        img_path = self.get_image_path(update)
        if img_path==None:
            update.messagebot.sendMessage(chat_id = update.message.chat_id, text = "Now you come to me, and you say: \"Mr. AI Bot, give me the answer, what is on the picture.\" But you don't ask with respect.")
            return
            
        img = cv2.imread(img_path)
        prediction = detect(self.net, self.meta, img_path.encode('ascii'))

        for k in prediction:
            # print("Name: ",k[0],"Predict %: ",k[1],"X: ",k[2][0],"Y: ",k[2][1],"W: ",k[2][2],"Z: ",k[2][3],'\n')
            
            # preprocessing coords from yolo to cv2 standart
            p1, p2, p3 = self.preprocess_coords(k[2])
            # drawing bounding boxes and writing names with probability
            cv2.rectangle(img, p1, p2, color, 2)
            name_and_prob = str(k[0].decode('ascii')) + " {0:.4f}".format(k[1])
            cv2.putText(img, name_and_prob, p3, font, 0.5, color, 1, cv2.LINE_AA)
        # saving image in local server directory
        marked_img_path = img_path + "1.jpg"
        cv2.imwrite(marked_img_path, img)
        # sending saved image as answer
        update.message.bot.send_photo(chat_id=update.message.chat_id, photo=open(marked_img_path, 'rb'))

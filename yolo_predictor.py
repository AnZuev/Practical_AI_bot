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
        self.cfg, self.weights, metap = self.prepare_all_paths(preffix, "cfg/yolov3.cfg", "yolov3.weights",

                                                                    "cfg/coco.data")
        self.meta = load_meta(metap)
        self.net = load_net(self.cfg, self.weights, 0)

    def preprocess_coords(self, coords):
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

    def get_image_object(self, update):
        message = update.message
        file_path = None
        if message.photo != None:
            file_path = message.bot.get_file(message.photo[2].file_id)
        return file_path

    def prepare_all_paths(self, path_to_darknet, path_to_cfg, path_to_weights, path_to_meta):
        prefix = path_to_darknet.encode('ascii')

        cfg_path = prefix + path_to_cfg.encode('ascii')
        weights_path = prefix + path_to_weights.encode('ascii')
        meta_path = prefix + path_to_meta.encode('ascii')

        return (cfg_path, weights_path, meta_path)

    def do_work(self, update):

        color = (0, 0, 255)
        font = cv2.FONT_HERSHEY_SIMPLEX

        img_telegram_object = self.get_image_object(update)

        r = requests.get(img_telegram_object.file_path)
        img_path = os.path.join(os.getcwd(), 'imgs', img_telegram_object.file_id)

        with open(img_path, 'wb') as f:
            f.write(r.content)
        f.close()

        img = cv2.imread(img_path)

        r = detect(self.net, self.meta, img_path.encode('ascii'))

        for k in r:
            # print("Name: ",k[0],"Predict %: ",k[1],"X: ",k[2][0],"Y: ",k[2][1],"W: ",k[2][2],"Z: ",k[2][3],'\n')
            p1, p2, p3 = self.preprocess_coords(k[2])
            cv2.rectangle(img, p1, p2, color, 2)
            name_and_prob = str(k[0].decode('ascii')) + " {0:.4f}".format(k[1])
            cv2.putText(img, name_and_prob, p3, font, 0.5, color, 1, cv2.LINE_AA)

        # convert img to send
        # _, niceimg = cv2.imencode(".jpg", img)
        # cv2.imshow("lol", cv2.imdecode(niceimg, 1))
        # cv2.waitKey()
        # decode img to save
        edited_img_path = img_path + "1.jpg"
        cv2.imwrite(edited_img_path, img)
        update.message.bot.send_photo(chat_id=update.message.chat_id, photo=open(edited_img_path, 'rb'))



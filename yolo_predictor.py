import sys, os
import cv2
from ctypes import *
import numpy as np

sys.path.append(os.path.join(os.getcwd(), 'python/'))
from darknet import *

color = (0, 0, 255)
font = cv2.FONT_HERSHEY_SIMPLEX

'''
def get_image_path(update, BOT_API_TOKEN):
    message=update.message
    file_path = None
    if message.photo!=None:
        file_path = message.bot.get_file(message.photo.file_path)
    return file_path
'''

def preprocess_coords(coords):
    width =  coords[2]
    height = coords[3]
    center_x = coords[0]
    center_y = coords[1]
    
    bottomLeft_x = center_x - (width / 2)
    bottomLeft_y = center_y - (height / 2)
    
    topRight_x = bottomLeft_x + width
    topRight_y = bottomLeft_y + height
    
    point1=(int(bottomLeft_x), int(bottomLeft_y))
    point2=(int(topRight_x), int(topRight_y))
    point3=(int(bottomLeft_x), int(bottomLeft_y)-5)
    
    return (point1, point2, point3)


def prepare_all_paths(path_to_darknet, path_to_cfg, path_to_weights, path_to_meta):
    prefix = path_to_darknet.encode('ascii')

    cfg_path = prefix + path_to_cfg.encode('ascii')
    weights_path = prefix + path_to_weights.encode('ascii')
    meta_path = prefix + path_to_meta.encode('ascii')

    return (cfg_path, weights_path, meta_path)
    

cfg, weights, metap = prepare_all_paths("/home/kostin_001/darknet/", "cfg/yolov3.cfg", "yolov3.weights", "cfg/coco.data")
net = load_net(cfg, weights, 0)
meta = load_meta(metap)


img_path = "/home/kostin_001/darknet/data/dog.jpg"
img = cv2.imread(img_path)

r = detect(net, meta, img_path.encode('ascii'))

# print bounding boxes

for k in r:
    # print("Name: ",k[0],"Predict %: ",k[1],"X: ",k[2][0],"Y: ",k[2][1],"W: ",k[2][2],"Z: ",k[2][3],'\n')
    p1, p2, p3 = preprocess_coords(k[2])
    cv2.rectangle(img, p1, p2, color, 2)
    name_and_prob =str(k[0].decode('ascii'))+" {0:.4f}".format(k[1])
    cv2.putText(img, name_and_prob, p3, font, 0.5, color, 1, cv2.LINE_AA)

cv2.imwrite("image.jpg", img)


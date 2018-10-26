import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
from shutil import copyfile
import numpy as np

train_ratio = 0.8

MAIN_DIR = 'objects'

classes = ["Palm"]


def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id):
    with open('%s/%s.xml'%(MAIN_DIR, image_id)) as in_file:
        tree = ET.parse(in_file)
    with open('%s/%s.txt'%(MAIN_DIR, image_id), 'w') as out_file:
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)

        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            if xmlbox == None:
                continue
            print(image_id + ': ' + obj.find('name').text)
            print('xmin: %s'%(float(xmlbox.find('xmin').text)))
            print('xmax: %s'%(float(xmlbox.find('xmax').text)))
            print('ymin: %s'%(float(xmlbox.find('ymin').text)))
            print('ymax: %s'%(float(xmlbox.find('ymax').text)))
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bb = convert((w,h), b)
            print(bb)
            out_file.write(str(cls_id) + " " + " ".join(["{0:.6f}".format(round(a,6)) for a in bb]) + '\n')

wd = getcwd()

image_ids = np.array([file[:-4] for file in os.listdir(MAIN_DIR) if file.endswith('.xml')])
order_image = np.random.permutation(len(image_ids))
train_index = image_ids[:int(len(image_ids) * train_ratio)]
val_index = image_ids[int(len(image_ids) * train_ratio):]
sets=[
    {'image_set': 'train', 'ids': train_index},
    {'image_set': 'val', 'ids': val_index}
]

for set in sets:
    image_set = set['image_set']
    image_ids = set['ids']
    list_file = open('%s.txt'%(image_set), 'w')
    with open('%s.txt'%(image_set), 'w') as list_file:
        for image_id in image_ids:
            list_file.write('%s/%s/%s.jpeg\n'%(wd, MAIN_DIR, image_id))
            convert_annotation(image_id)

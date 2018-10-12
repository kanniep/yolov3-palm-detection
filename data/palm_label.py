import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
from shutil import copyfile
import numpy as np

train_ratio = 0.8

classes = ["Palm"]


def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    if x == 0:
        x += 1e-6
    w = w*dw
    if w == 0:
        w += 1e-6
    y = y*dh
    if y == 0:
        y += 1e-6
    h = h*dh
    if h == 0:
        h += 1e-6
    return (x,y,w,h)

def convert_annotation(image_id):
    in_file = open('Annotations/%s.xml'%(image_id))
    out_file = open('labels/%s.txt'%(image_id), 'w')
    tree=ET.parse(in_file)
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
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()

if not os.path.exists('ImageSets/Main'):
    os.makedirs('ImageSets/Main')
if not os.path.exists('JPEGImages'):
    os.makedirs('JPEGImages')
if not os.path.exists('labels'):
    os.makedirs('labels')
if not os.path.exists('Annotations'):
    os.makedirs('Annotations')

image_ids = np.array([file[:-4] for file in os.listdir('export/') if file.endswith('.xml')])
order_image = np.random.permutation(len(image_ids))
train_index = image_ids[:int(len(image_ids) * train_ratio)]
val_index = image_ids[int(len(image_ids) * train_ratio):]
sets=[
        {'image_set': 'train', 'ids': train_index},
        {'image_set': 'val', 'ids': val_index}
    ]

with open('ImageSets/Main/%s.txt'%('train'), 'w') as train_ids_file:
    for image_id in train_index:
        train_ids_file.write('%s\n'%(image_id))
        copyfile('export/%s.jpeg'%(image_id), 'JPEGImages/%s.jpeg'%(image_id))
        copyfile('export/%s.jpeg'%(image_id), 'labels/%s.jpeg'%(image_id))
        copyfile('export/%s.xml'%(image_id), 'Annotations/%s.xml'%(image_id))
with open('ImageSets/Main/%s.txt'%('val'), 'w') as val_ids_file:
    for image_id in val_index:
        val_ids_file.write('%s\n'%(image_id))
        copyfile('export/%s.jpeg'%(image_id), 'JPEGImages/%s.jpeg'%(image_id))
        copyfile('export/%s.jpeg'%(image_id), 'labels/%s.jpeg'%(image_id))
        copyfile('export/%s.xml'%(image_id), 'Annotations/%s.xml'%(image_id))

for set in sets:
    image_set = set['image_set']
    image_ids = set['ids']
    list_file = open('%s.txt'%(image_set), 'w')
    for image_id in image_ids:
        list_file.write('%s/JPEGImages/%s.jpeg\n'%(wd, image_id))
        convert_annotation(image_id)
    list_file.close()

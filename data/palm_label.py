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

def convert_annotation(year, image_id):
    in_file = open('VOCdevkit/VOC%s/Annotations/%s.xml'%(year, image_id))
    out_file = open('VOCdevkit/VOC%s/labels/%s.txt'%(year, image_id), 'w')
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

if not os.path.exists('VOCdevkit/VOC2018/ImageSets/Main'):
    os.makedirs('VOCdevkit/VOC2018/ImageSets/Main')
if not os.path.exists('VOCdevkit/VOC2018/JPEGImages'):
    os.makedirs('VOCdevkit/VOC2018/JPEGImages')
if not os.path.exists('VOCdevkit/VOC2018/labels'):
    os.makedirs('VOCdevkit/VOC2018/labels')
if not os.path.exists('VOCdevkit/VOC2018/Annotations'):
    os.makedirs('VOCdevkit/VOC2018/Annotations')

image_ids = np.array([file[:-4] for file in os.listdir('export/') if file.endswith('.xml')])
order_image = np.random.permutation(len(image_ids))
train_index = image_ids[:int(len(image_ids) * train_ratio)]
val_index = image_ids[int(len(image_ids) * train_ratio):]
sets=[
        {'year': '2018', 'image_set': 'train', 'ids': train_index},
        {'year': '2018', 'image_set': 'val', 'ids': val_index}
    ]

with open('VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%('2018', 'train'), 'w') as train_ids_file:
    for image_id in train_index:
        train_ids_file.write('%s\n'%(image_id))
        copyfile('export/%s.jpeg'%(image_id), 'VOCdevkit/VOC2018/JPEGImages/%s.jpeg'%(image_id))
        copyfile('export/%s.jpeg'%(image_id), 'VOCdevkit/VOC2018/labels/%s.jpeg'%(image_id))
        copyfile('export/%s.xml'%(image_id), 'VOCdevkit/VOC2018/Annotations/%s.xml'%(image_id))
with open('VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%('2018', 'val'), 'w') as val_ids_file:
    for image_id in val_index:
        val_ids_file.write('%s\n'%(image_id))
        copyfile('export/%s.jpeg'%(image_id), 'VOCdevkit/VOC2018/JPEGImages/%s.jpeg'%(image_id))
        copyfile('export/%s.jpeg'%(image_id), 'VOCdevkit/VOC2018/labels/%s.jpeg'%(image_id))
        copyfile('export/%s.xml'%(image_id), 'VOCdevkit/VOC2018/Annotations/%s.xml'%(image_id))

for set in sets:
    year = set['year']
    image_set = set['image_set']
    image_ids = set['ids']
    if not os.path.exists('VOCdevkit/VOC%s/labels/'%(year)):
        os.makedirs('VOCdevkit/VOC%s/labels/'%(year))
    # image_ids = open('VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
    list_file = open('%s_%s.txt'%(year, image_set), 'w')
    for image_id in image_ids:
        list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpeg\n'%(wd, year, image_id))
        convert_annotation(year, image_id)
    list_file.close()

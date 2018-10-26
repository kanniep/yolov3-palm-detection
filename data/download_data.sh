#!/bin/bash
link=$1
tarfile='export_data.tar.gz'
wget -O $tarfile $link
tar zxvf $tarfile
mv export objects
python3 palm_label.py
cd ..
wget https://pjreddie.com/media/files/darknet53.conv.74

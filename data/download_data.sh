#!/bin/bash
link=$1
tarfile='export_data.tar.gz'
wget -O $tarfile $link
tar zxvf $tarfile 'export'
python3 palm_label.py

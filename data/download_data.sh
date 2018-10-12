#!/bin/bash
link=$1
tarfile='export_data.tar.gz'
wget $link > $tarfile
tar zxvf $tarfile 'export'
python3 palm_lable.py

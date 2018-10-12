#!/bin/bash
link=$0
tarfile='export_data.tar.gz'
wget $link > $tarfile
tar zxvf $tarfile 'export'
python3 palm_lable.py
https://storage.googleapis.com/labelbox-exports/cjn36v6h32fm30780jy7njsrl/cjn36vqgi2fss0780ooua0dmq/export-voc-2018-10-10T15%3A40%3A40.103490.tar.gz

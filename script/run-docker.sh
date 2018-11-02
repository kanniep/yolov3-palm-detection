#/bin/bash
nvidia-docker run -it -d -v /home/kannie/backup:/root/backup --name palm kannie/yolov3-palm-detection

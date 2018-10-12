FROM kannie/darknet-yolov3

WORKDIR /tmp
RUN git clone https://github.com/kanniep/yolov3-palm-detection.git
RUN mv yolov3-palm-detection/* /root/
WORKDIR /root

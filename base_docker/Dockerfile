FROM nvidia/cuda:9.1-cudnn7-devel

# apt-get
RUN apt-get update
RUN apt-get install wget git unzip build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev -y
RUN apt-get clean

# build darknet
WORKDIR /tmp
RUN git clone https://github.com/AlexeyAB/darknet.git
WORKDIR /tmp/darknet
RUN sed -ie "s/GPU=0/GPU=1/g" Makefile
RUN sed -ie "s/CUDNN=0/CUDNN=1/g" Makefile
RUN sed -ie "s/CUDNN_HALF=0/CUDNN_HALF=1/g" Makefile
RUN sed -ie "s/AVX=0/AVX=1/g" Makefile
RUN sed -ie "s/OPENMP=0/OPENMP=1/g" Makefile
RUN make
RUN cp darknet ~/

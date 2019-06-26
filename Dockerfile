ARG CUDA_VERSION=10.0

# 拉取特定版本的cuda，需要里面的nvcc
FROM nvidia/cuda:${CUDA_VERSION}-devel

RUN apt-get update && apt-get install -y \
    python3-pip \
    git

RUN pip install torch

WORKDIR /root

# https://github.com/NVIDIA/apex#linux
RUN git clone https://github.com/NVIDIA/apex
RUN cd apex
RUN pip install -v --global-option="--cpp_ext" --global-option="--cuda_ext" ./

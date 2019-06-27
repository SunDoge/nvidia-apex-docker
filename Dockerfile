ARG CUDA_VERSION=10.0
ARG PYTHON_VERSION=3.7
# 空字符串，下载最新pytorch
ARG TORCH_VERSION=1.1.0

# 拉取特定版本的cuda，需要里面的nvcc
FROM nvidia/cuda:${CUDA_VERSION}-devel

RUN apt-get update --fix-missing

RUN apt-get install -y git wget

WORKDIR /root

# 更换清华源
# https://hub.docker.com/r/continuumio/miniconda/dockerfile
# https://github.com/conda/conda-docker/blob/master/miniconda3/debian/Dockerfile
RUN wget --quiet https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -bfp /usr/local && \
    rm ~/miniconda.sh

RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ && \
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ && \
    conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/ && \
    conda config --set show_channel_urls yes

RUN conda install -y python=${PYTHON_VERSION}
RUN conda install -y pytorch=${TORCH_VERSION} cudatoolkit=${CUDA_VERSION} -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/

# https://github.com/NVIDIA/apex#linux，保留cache
RUN git clone --depth=1 https://github.com/NVIDIA/apex
# RUN cd apex && pip install -v --global-option="--cpp_ext" --global-option="--cuda_ext" ./
RUN cd apex && \
    python setup.py bdist_wheel --cpp_ext --cuda_ext





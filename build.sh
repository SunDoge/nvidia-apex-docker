#!/bin/bash

build_docker_image() {
    docker build . -t sundoge/apex:cuda$1-py$2 \
    --build-arg CUDA_VERSION=$1 \
    --build-arg PYTHON_VERSION=$2 
}

# build_docker_image 10.0 3.6
# build_docker_image 10.0 3.7
build_docker_image 10.1 3.7
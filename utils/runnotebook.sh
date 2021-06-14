#!/bin/bash
# Runs a Jupyter notebook server for a prebuilt docker image named 'myproject'
# see script builddocker.sh for how to build the image
# it also maps the current directory to a folder within the docker image

GPU=$(sudo lshw -numeric -C display)

if [[ $GPU == *"NVIDIA"* ]]; then
    echo "Trying to run with GPU (make sure you have nvidia-docker installed)"
    sudo docker run --gpus all -u $(id -u):$(id -g) -v $(pwd):/tf -it --rm -p 8888:8888 myproject
else
    echo "Running with CPU only"
    sudo docker run -u $(id -u):$(id -g) -v $(pwd):/tf -it --rm -p 8888:8888 myproject
fi

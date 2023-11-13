#!/bin/bash

# Build docker image
# sudo docker build -t ece512 .

# Save latest container to image
# sudo docker ps
# sudo docker commit <container id> ece512:latest

# Delete old image
# sudo docker images
# sudo docker rmi <image id>

# Launch docker container
sudo docker run -it --rm \
    -v /mnt/d/nachuan3/bin/ece512:/workspace/ece512 \
    -v /mnt/d/nachuan3/bin/xilinx:/workspace/xilinx \
    -v /home/janux/.Xilinx:/root/.Xilinx \
    -w /workspace/ece512/sims/verilator \
    -e PATH="/workspace/xilinx/Vivado/2021.1/bin:${PATH}" \
    ece512:latest bash

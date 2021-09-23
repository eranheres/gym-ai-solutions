ARG CACHEBUST=1

# Specifies base image and tag
FROM tensorflow/tensorflow:2.2.0rc1-py3
WORKDIR /root

# Copies the trainer code to the docker image.
COPY requirements.txt .

# python-numpy python-dev cmake zlib1g-dev libjpeg-dev xvfb ffmpeg xorg-dev python-opengl libboost-all-dev libsdl2-dev swig
RUN apt-get update && apt-get install -y \
    xvfb ffmpeg xorg-dev python-opengl swig
# Installs additional packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apt-get install x11-utils

ARG CACHEBUST
COPY gym-rl ./gym-rl

# Sets up the entry point to invoke the trainer.
ENTRYPOINT ["python", "-m", "gym-rl.task", "train"]

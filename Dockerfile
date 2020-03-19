# Specifies base image and tag
FROM tensorflow/tensorflow:latest-py3
WORKDIR /root

# Copies the trainer code to the docker image.
COPY requirements.txt .
COPY gym-rl ./gym-rl

# Installs additional packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Sets up the entry point to invoke the trainer.
ENTRYPOINT ["python", "test.py"]
export IP=$(ifconfig en0 | grep -w inet | awk '{print $2}')
xhost + $IP
export PROJECT_ID=$(gcloud config list project --format "value(core.project)")
export IMAGE_REPO_NAME=gym-ai-solution
export IMAGE_TAG=latest
export IMAGE_URI=gcr.io/$PROJECT_ID/$IMAGE_REPO_NAME:$IMAGE_TAG

docker build -f Dockerfile -t $IMAGE_URI ./
docker run --name=gym-ai-solutions --rm -t \
       -e DISPLAY=10.100.102.15:0 \
       --privileged=true \
       -v /tmp/.X11-unix:/tmp/.X11-unix \
       $IMAGE_URI

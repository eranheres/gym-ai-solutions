export PROJECT_ID=$(gcloud config list project --format "value(core.project)")
export IMAGE_REPO_NAME=example_custom_container_image
export IMAGE_TAG=trainer_image_tag
export IMAGE_URI=gcr.io/$PROJECT_ID/$IMAGE_REPO_NAME:$IMAGE_TAG


docker run -e DISPLAY=${ip}:0 -v /tmp/.X11-unix:/tmp/.X11-unix $IMAGE_TAG

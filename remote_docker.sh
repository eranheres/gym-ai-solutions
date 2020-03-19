export PROJECT_ID=$(gcloud config list project --format "value(core.project)")
export IMAGE_REPO_NAME=example_custom_container_image
export IMAGE_TAG=trainer_image_tag
export IMAGE_URI=gcr.io/$PROJECT_ID/$IMAGE_REPO_NAME:$IMAGE_TAG

docker build -f Dockerfile -t $IMAGE_URI ./

export BUCKET_NAME=custom_containers
export MODEL_DIR=example_model_$(date +%Y%m%d_%H%M%S)

gcloud ai-platform jobs submit training $JOB_NAME \
  --region $REGION \
  --master-image-uri $IMAGE_URI \
  -- \
  --model-dir=gs://$BUCKET_NAME/$MODEL_DIR \
  --epochs=10

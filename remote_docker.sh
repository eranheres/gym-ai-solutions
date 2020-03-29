export PROJECT_ID=$(gcloud config list project --format "value(core.project)")
export IMAGE_REPO_NAME=gym-ai-solution
export IMAGE_TAG=latest
export IMAGE_URI=gcr.io/$PROJECT_ID/$IMAGE_REPO_NAME:$IMAGE_TAG
export REGION="us-east1"
now=$(date +"%Y%m%d_%H%M%S")
JOB_NAME="eran_job_$now"

export BUCKET_NAME=crazylabs-testeran-ml-exports
export JOB_DIR=model_$JOB_NAME

docker build -f Dockerfile -t $IMAGE_URI ./
docker push $IMAGE_URI

gcloud ai-platform jobs submit training $JOB_NAME \
  --region $REGION \
  --master-image-uri $IMAGE_URI \
  --stream-logs \
  -- \
  gym-rl/envs_configs/MountainCar-v0.json \
  --save-render \
  --gcp \
  --job-dir=gs://$BUCKET_NAME/$JOB_DIR

gcloud ai-platform jobs stream-logs $JOB_NAME
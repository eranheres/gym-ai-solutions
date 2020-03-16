T=`date "+%Y%m%d%H%M%S"`
JOB_NAME="job_"$T
BUCKET_NAME="crazylabs-testeran-ml-models"
JOB_DIR="gs://$BUCKET_NAME/keras-job-dir"
REGION="us-central1"

echo "starting job:"$JOB_NAME
gcloud ai-platform jobs submit training $JOB_NAME \
  --package-path gym-rl \
  --module-name gym-rl.acrobot_v1 \
  --region $REGION \
  --python-version 3.7 \
  --runtime-version 2.1 \
  --job-dir $JOB_DIR \
  --stream-logs \
  -- \
  train \
  --render gif \
  --headless
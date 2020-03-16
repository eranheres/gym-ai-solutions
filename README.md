## Gym - solutions
This project aims to provide entire set of optimal solutions for GymAI environments.To begin with not all solutions here
are optimal, rather than just solutions.
All projects can run on both local and cloud (GCP).

### Setup (local)
```
python3 -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
```

### Setup (google cloud)
Follow the following guidelines to setup account, service-account etc: https://cloud.google.com/ai-platform/docs/getting-started-keras?authuser=1

```
BUCKET_NAME="<bucket-name>"
export GOOGLE_APPLICATION_CREDENTIALS="credentials-folder"
REGION="us-central1"
```

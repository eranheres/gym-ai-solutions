## Gym - solutions
This project aims to provide entire set of optimal solutions for GymAI environments.To begin with not all solutions here
are optimal. This is an on-going project... not all solutions are available, more to come.
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

### Run locally
TBD

### Run docker locally (mac)

```
xhost + 10.100.102.15
docker run --name=gym-ai-solutions -it --rm -e DISPLAY=10.100.102.15:0 --privileged=true -v /tmp/.X11-unix:/tmp/.X11-unix gym-ai-solutions
```

### Run remotely

```
remote.sh
```

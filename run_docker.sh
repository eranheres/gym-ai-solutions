#!/bin/bash -v

RUN_REMOTE=0
export PROJECT_ID=$(gcloud config list project --format "value(core.project)")
export IMAGE_NAME=gym-ai-solution
export MODEL_DIR=example_model_$(date +%Y%m%d_%H%M%S)
export CONTAINER=$IMAGE_NAME-container

show_help() {
cat << EOF
Usage: [-h] [--remote] [-b BUCKET] [-r REPOSITORY] [-f DOCKER_RUN_FLAGS]

This script is a convenience script to run Docker images localy or remotly

Options:

  -h             Display this help and exit.
  --remote       Flag to run container remotly on GCP
  -b             Bucket name
  -r             Repository name
  -f             Extra arguments to pass to 'docker run'. E.g.
                 --env="APP=glxgears"
EOF
}

while [ $# -gt 0 ]; do
	case "$1" in
		-h)
			show_help
			exit 0
			;;
		-b)
			bucket=$2
			shift
			;;
		-r)
			IMAGE_REPO_NAME=$2
			shift
			;;
		--remote)
		  remote = 1
			;;
		-r)
			extra_run_args="$extra_run_args $2"
			shift
			;;
		-q)
			quiet=1
			;;
		*)
			show_help >&2
			exit 1
			;;
	esac
	shift
done


which docker 2>&1 >/dev/null
if [ $? -ne 0 ]; then
	echo "Error: the 'docker' command was not found.  Please install docker."
	exit 1
fi

cleanup() {
	docker stop $CONTAINER >/dev/null
	docker rm $CONTAINER >/dev/null
}

if [ $RUN_REMOTE -eq 0 ]; then
  running=$(docker ps -a -q --filter "name=${CONTAINER}")
  if [ -n "$running" ]; then
    cleanup
  fi

  pwd_dir="$(pwd)"
  mount_local=""
  if [ "${os}" = "Linux" ] || [ "${os}" = "Darwin" ]; then
    mount_local=" -v ${pwd_dir}:/home/user/work "
  fi
  port_arg=""
  if [ -n "$port" ]; then
    port_arg="-p $port:6080"
  fi

  echo docker run -d --name $CONTAINER ${mount_local} $extra_run_args $IMAGE_NAME
  docker run -d --name $CONTAINER ${mount_local} $extra_run_args $IMAGE_NAME

  print_app_output() {
    docker cp $container:/var/log/supervisor/graphical-app-launcher.log - \
      | tar xO
    result=$(docker cp $container:/tmp/graphical-app.return_code - \
      | tar xO)
    cleanup
    exit $result
  }

  trap "docker stop $container >/dev/null && print_app_output" SIGINT SIGTERM

  docker wait $CONTAINER >/dev/null

  print_app_output
else
  echo Not supporting remote, yet...
fi

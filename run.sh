# Prepare environment


# docker volume create shared
# Run compoes with environment variables file.

export WORKERS=$1

rm /var/lib/docker/volumes/shared/_data/*

start_exp() {
  # Remove previous output

  export WORKERS=$1
  export ENVFILE=$2

  echo "Workers: $WORKERS, ENV_FILE: $ENVFILE"

  cat .env.test > .env
  echo WORKERS=${WORKERS} >> .env
        # Detached
  docker-compose --env-file ./$ENVFILE up -d --build --scale queue_sim=$WORKERS
        # Attached
  # docker-compose --env-file ./$ENVFILE up --build --scale queue_sim=$WORKERS
  rm ./.env
  
  sleep 5s
  
  docker-compose down
}


export ENVFILE=.env.rr
start_exp $WORKERS $ENVFILE

export ENVFILE=.env.r
start_exp $WORKERS $ENVFILE

export ENVFILE=.env.tc
start_exp $WORKERS $ENVFILE

./results.sh

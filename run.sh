# Prepare environment

# Remove previous output
rm /var/lib/docker/volumes/shared/_data/T/queue_output.workers

# docker volume create shared
# Run compoes with environment variables file.

export WORKERS=$1
cat .env.test > .env
echo WORKERS=${WORKERS} >> .env
      # Detached
docker-compose --env-file ./.env.general up -d --build --scale queue_sim=$WORKERS
      # Attached
rm ./.env

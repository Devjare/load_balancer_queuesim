# Prepare environment
# docker volume create shared
# Run compoes with environment variables file.
export WORKERS=$1
cat .env.test > .env
echo WORKERS=${WORKERS} >> .env
      # Detached
docker-compose --env-file ./.env.test up -d --build --scale queue_sim=$WORKERS
      # Attached
# docker-compose --env-file ./.env up --build --scale queue_sim=$WORKERS
rm ./.env

echo "\nQUEUE OUTPUT: \n"
cat /var/lib/docker/volumes/shared/_data/T1/queue_output.workers

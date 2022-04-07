# Prepare environment
# docker volume create shared
# Run compoes with environment variables file.
export WORKERS=$1
# echo WORKERS=${WORKERS} >> .env.test
      # Detached
# docker-compose --env-file ./.env.test -env WORKERS=${WORKERS} up -d --build --scale queue_sim=$WORKERS
      # Attached
docker-compose --env-file ./.env.test up --build --scale queue_sim=$WORKERS

echo "\nQUEUE OUTPUT: \n"
cat /var/lib/docker/volumes/shared/_data/queue_output_worker_*

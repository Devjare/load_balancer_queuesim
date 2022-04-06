# Prepare environment
# docker volume create shared
# Run compoes with environment variables file.
docker-compose --env-file ./.env.test up -d --build

# Execution order.
docker container exec load_balancer_trace_gen_1 /bin/ash generate.sh
docker container start load_balancer_middleware_1
docker container exec load_balancer_queue_sim_1 /bin/ash simul.sh

echo "\nQUEUE OUTPUT: \n"
cat /home/devjare/.local/share/docker/volumes/shared/_data/queue_output

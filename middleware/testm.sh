docker image build -t mware:v1 .
docker container run -v shared:/middleware/output mware:v1

# Load balancer with python on a containerized environment.

## Description

Middleware developed in order to make communication of two different programs possible.
The first program runs a generator of random clientes requests on continuos arrivals,
while the second one simulates a request and service queue. 

The goal of the middleware implemented here is to prepare an input to the second program
utilizing the output of the first program. Besides making the connection between those two,
the implementations is made with docker and docker-compose aiming to make the solution available
as a distributed system where is possible to impelement a load balancing method.

## General Funcionality

The funcitonality of the code follows the next flow:

Run traceGenerator - output -> Run middleware.

where:
- traceGenerator:
  - input: arguments to generate traces(listed on readme of that code.)
  - process: generate a trace file.
  - output: trace file as csv.
- middleware:
  - input: trace file from traceGenerator.
  - process:
    1. separate trace on number of woken workers.
    2. call execution of queue simulator via http request(Using docker remote API) with
    worker ID. 
  - output: None

- ***worker:*** Implementaion(Container) of the queue simulator 

## Execution requirements.

In order to execute(up) the complete environment a previous set up is needed:

1. **Setup environment variables:** On the file *.env.general* there are a number of variables, which
  are on the most part to execute the trace generator: SAMPLES, SIZE, INTER_ARRIVAL, READ_RATIO, SAS, DISTRIBUTION, MEAN, STDEV, CONCURRENCY. 
  The variables: ST, DELAY are the ones needed as input of the queue simulator. While the last ones: SERVER_IP, SERVER_PORT, API_VERSION are required for the docker remote API to work, they must be specified to the server which is executing docker.

  If the docker remote API version is unknow but the port and IP Where it is executing, making a request to http://IP:PORT/version returns a JSON with information about the docker daemon running. The key "ApiVersion":"1.41" contains the value which must be assigned, with a "v" at the begging, to API_VERSION environment variable(e.g API_VERSION=v1.41).

# Running the code.

To run the code, execute the bash script *run.sh* with superuser permissions. The permissions are needed to read from the docker directory where the data is stored.

One paramter is needed to run the script, that is the number of instances(workers) to make avaible(set "up" with compose).

> sudo ./run.sh <WORKERS>

If the permissions were given correctly, then the results should be saved on the docker root directoy under the volume *shared*.
In order to see the results, execute similarly with super user permissions the script *results.sh*. It should display something like:

![Report results per worker.](/images/results_sc.png)

import pandas as pd
import numpy as np
import os
import requests

RANDOM = 'R'
ROUND_ROBIN = 'RR'
HASH = "H"

DEFAULT_WORKERS = 3
DEFAULT_ST = 10
DEFAULT_DELAY = 10
DEFAULT_IP = "unix://" # Directly on unix socket.
DEFAULT_PORT = "56789" # Directly on unix socket.
DEFAULT_API = "1.41" # Directly on unix socket.

no_workers = int(os.getenv("WORKERS", DEFAULT_WORKERS))
mean_service = int(os.getenv("ST", DEFAULT_ST))
num_delays = int(os.getenv("DELAY", DEFAULT_DELAY))

SERVER_IP = os.getenv("SERVER_IP", DEFAULT_IP)
SERVER_PORT = os.getenv("SERVER_PORT", DEFAULT_PORT)
API_VERSION = os.getenv("API_VERSION")
endpoint = "containers"


def distribute_traces(data, no_workers, balancer=RANDOM):
    per_worker_traces = {i+1:[] for i in range(no_workers)}
    if(balancer == ROUND_ROBIN):
        for i in range(len(data)):
            j = i % no_workers + 1 # Container names from compose, always end in 1 at least, not 0
            per_worker_traces[j].append(data[i])

    # Append mean at the end.

    for worker in per_worker_traces:
        inter_arrivals = per_worker_traces[worker]
        print("Inter arrivals: %s, mean: %d" % (inter_arrivals, np.mean(inter_arrivals)))
        differences = np.diff(inter_arrivals)
        print("Differences: %s, mean: %d" % (differences, np.mean(differences)))
        per_worker_traces[worker].append(np.mean(differences))

    return per_worker_traces

def get_interarrivals(data, workers):
    inter_arrivals = [data[0]]

    per_worker_traces = distribute_traces(data, workers, balancer=ROUND_ROBIN)
 
    return per_worker_traces


names = ["interarrival", "worker", "operation", "space", "filesize"]
data = pd.read_csv("output/trace.csv", names=names, header=None)

def get_id_worker(worker_number):
    """
    Get the container id of the worker with the assigned number
    from the round robin.
    """
    # request asks for all containers that have the base image of all our containers.
    request = "json?all=1&filters=%7B%22ancestor%22%3A%5B%22queuesim%3Av1%22%5D%7D"
    url = "http://{}:{}/{}/{}/{}".format(SERVER_IP,SERVER_PORT,API_VERSION,endpoint,request)
    print("Getting: ", url)
    response = requests.get(url)
    data = response.json()
   
    print(data)
    for d in data:
        # print("Id: %s, Container Name: %s, Image: %s" 
                # % (d["Id"], d["Names"][0], d["Image"]))
        worker_no = d["Names"][0][-1] # Number of the worker given by compose.
        Id = d["Id"] # Number of the worker given by compose.
        if(worker_no == str(worker_number)):
            print("Adding to worker: ", worker_no)
            return Id

def request_sim(worker_no, worker_id, interarrival, servicetime, num_delay):
    # Create command for simulator.
    headers = { 'Content-Type': 'application/json'}
    json_data = {
        'Cmd': [
            '/bin/ash',
            './simul.sh',
        ],
        'Env': [
            "INTERARRIVAL=" + str(interarrival),
            "SERVICETIME=" + str(servicetime),
            "NUM_DELAY=" + str(num_delay),
            "WORKER=" + str(worker_no)
    ],
    }
    # url = 'http://192.168.43.47:56789/v1.41/containers/' + worker_id + '/exec'
    url = "http://{}:{}/{}/{}/{}/exec".format(SERVER_IP,SERVER_PORT,API_VERSION,endpoint,worker_id)
    response = requests.post(url, headers=headers, json=json_data)
    
    rd = response.json()
    exec_id = rd["Id"]

    # Exec command simulator
    json_data = {}
    url = "http://{}:{}/{}/exec/{}/start".format(SERVER_IP,SERVER_PORT,API_VERSION,exec_id)
    response = requests.post(url, headers=headers, json=json_data)
    print(response.content)
    return response
    
# inter_arrival_mean = np.mean(inter_arrivals) / 1000 # milliseconds to seconds

arrivals = data['interarrival']
inter_arrivals = get_interarrivals(arrivals, no_workers)
print("Inter Arrivals: ", inter_arrivals)
print("Workers: %d, service_Time: %d, delays: %d" % (no_workers, mean_service, num_delays))

for i in inter_arrivals:
   # last index is mean 
    worker_id = get_id_worker(i)
    request_sim(i, worker_id, inter_arrivals[i][-1], mean_service, num_delays)
   # with open("./output/input", "w") as f:
   #      inpt = "" + str(inter_arrival_mean) + " " + str(mean_service) + " " + str(num_delays) + "\n"
   #      f.write(inpt)


# PRocess: 
# 1. generate trace
#   1.1 Save tracefile as csv on shared volume
# 2. Execute middle ware.
#   2.1 Middleware reads trace csv from shared volume
#   2.2 Middleware process csv.
#   2.3 Middleware geneartes file with input for QueueSimulator.
#   2.4 Middleware saves file with input on shared volume.
# 3. Execute Queue Simulator
#   3.1 Queue simulator takes as input file on shared volume (With pipe)

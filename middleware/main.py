import pandas as pd
import numpy as np
import os
import requests
import math
import random

RANDOM = 'R'
ROUND_ROBIN = 'RR'
TWO_CHOICES = "TC"

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
BALANCER = os.getenv("BALANCER")
endpoint = "containers"


def distribute_traces(data, no_workers, balancer=RANDOM):
    per_worker_traces = {i+1:[] for i in range(no_workers)}
    for i in range(len(data)):
        j = 0
        if(balancer == ROUND_ROBIN):
            j = i % no_workers + 1 # Container names from compose, always end in 1 at least, not 0
            per_worker_traces[j].append(data[i])
        elif(balancer == RANDOM):
            j = random.randint(1, no_workers) 
            per_worker_traces[j].append(data[i])
        else:
            j1 = random.randint(1, no_workers) 
            j2 = random.randint(1, no_workers) 
            
            j1_queue = len(per_worker_traces[j1])
            j2_queue = len(per_worker_traces[j2])
            
            print(f"Worker: {j1} queue: {j1_queue}")
            print(f"Worker: {j2} queue: {j2_queue}")
            if(j1_queue > j2_queue):
                # Append to j2 worker since j1 has a longer queue
                per_worker_traces[j2].append(data[i])
                j = j2
            else:
                per_worker_traces[j1].append(data[i])
                j = j1
        
        print(f"\tAdding trace: {data[i]} to worker {j}")


    # Append mean at the end.

    for worker in per_worker_traces:
        inter_arrivals = per_worker_traces[worker]
        print("Inter arrivals: %s, mean: %d" % (len(inter_arrivals), np.mean(inter_arrivals)))
        differences = np.diff(inter_arrivals)
        print("Differences: %s, mean: %d" % (len(differences), np.mean(differences)))
        per_worker_traces[worker].append(np.mean(differences))

    return per_worker_traces

def get_interarrivals(data, workers):
    inter_arrivals = [data[0]]

    per_worker_traces = distribute_traces(data, workers, balancer=BALANCER)
 
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
   
    for d in data:
        # print("Id: %s, Container Name: %s, Image: %s" 
                # % (d["Id"], d["Names"][0], d["Image"]))
        worker_no = d["Names"][0].split("_")[-1] # Number of the worker given by compose.
        Id = d["Id"] # Number of the worker given by compose.
        if(worker_no == str(worker_number)):
            print("Adding to worker: ", worker_no)
            return Id

def request_sim(worker_no, worker_id, interarrival, servicetime, num_delay, no_workers):
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
            "WORKER=" + str(worker_no),
            "WORKERS=" + str(no_workers)
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
    return response
    
# inter_arrival_mean = np.mean(inter_arrivals) / 1000 # milliseconds to seconds

arrivals = data['interarrival']
inter_arrivals = get_interarrivals(arrivals, no_workers)
for i in range(1, no_workers+1):
    print(f"Inter Arrivals worker[{i}]: \n", len(inter_arrivals[i]))
print("Workers: %d, service_Time: %d, delays: %d" % (no_workers, mean_service, num_delays))

for i in inter_arrivals:
   # last index is mean 
    worker_id = get_id_worker(i)
    # change scale to make more viable results
    mean_inter_arrival = round(inter_arrivals[i][-1] / 1000, 3)
    request_sim(i, worker_id, mean_inter_arrival, mean_service, num_delays, no_workers)
   # with open("./output/input", "w") as f:
   #      inpt = "" + str(inter_arrival_mean) + " " + str(mean_service) + " " + str(num_delays) + "\n"
   #      f.write(inpt)


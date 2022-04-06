import pandas as pd
import numpy as np

def get_interarrivals(data):
    inter_arrivals = [data[0]]
    for i in range(1, len(data)):
        inter_arrivals.append(data[i] - data[i-1])
    
    return inter_arrivals


names = ["interarrival", "worker", "operation", "space", "filesize"]
data = pd.read_csv("output/trace.csv", names=names, header=None)

arrivals = data['interarrival']
inter_arrivals = get_interarrivals(arrivals)
print("Inter Arrivals: ", inter_arrivals)

inter_arrival_mean = np.mean(inter_arrivals) / 1000 # milliseconds to seconds
mean_service = 1
num_delays = len(inter_arrivals)

with open("./output/input", "w") as f:
    inpt = "" + str(inter_arrival_mean) + " " + str(mean_service) + " " + str(num_delays) + "\n"
    f.write(inpt)

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

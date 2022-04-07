import requests

# With unix sockets
# curl --unix-socket /var/run/docker.sock http://v1.41/containers/json'?all=1&filters=%7B%22ancestor%22%3A%5B%22queuesim%3Av1%22%5D%7D'

# on remote host.
# curl http://148.247.204.201:56789/v1.41/containers/json'?all=1&filters=%7B%22ancestor%22%3A%5B%22queuesim%3Av1%22%5D%7D'
ip = "148.247.204.201"
# http://192.168.43.47:56789/1.41/containers/json?all=1&filters=%7B%22ancestor%22%3A%5B%22queue_sim%3Av1%22%5D%7D

port = 56789
endpoint = "containers"
request = "json?all=1&filters=%7B%22ancestor%22%3A%5B%22queuesim%3Av1%22%5D%7D"
# url = "http://" + ip + ":" + str(port) + "/v1.41/" + endpoint + "/" + request

def build_req_str(ip, port, endpoint, req):
    url = "http://" + ip + ":" + str(port) + "/v1.41/" + endpoint + "/" + req
    return url

url = build_req_str(ip, port, endpoint, request)

# print(response)
# print(data)

def get_id_worker(worker_number):
    """
    Get the container id of the worker with the assigned number
    from the round robin.
    """
    response = requests.get(url)
    data = response.json()
   
    for d in data:
        print("Id: %s, Container Name: %s, Image: %s" % (d["Id"], d["Names"][0], d["Image"]))
        worker_no = d["Names"][0][-1] # Number of the worker given by compose.
        Id = d["Id"] # Number of the worker given by compose.
        if(worker_no == str(worker_number)):
            print("Adding to worker: ", worker_no)
            return Id


turn = 3
worker_id = get_id_worker(turn)
print(f"Id of worker: {worker_id}")
request = f"{worker_id}/exec"
# data = { "Cmd": ["/bin/ash", "simul.sh"] }
# url = build_req_str(ip, port, endpoint, request)
print("Request post: ", url)
# response = requests.get(url, data=data)
# headers = {'Content-type': 'application/json'}
# response = requests.post(url, data=data, headers=headers)

headers = {
    # Already added when you pass json= but not when you pass data=
    'Content-Type': 'application/json',
}

json_data = {
    'Cmd': [
        '/bin/ash',
        './simul.sh',
    ],
    'Env': [
        "INTERARRIVAL=6.17",
        "SERVICETIME=10",
        "NUM_DELAY=10"
    ],
}
url = 'http://192.168.43.47:56789/v1.41/containers/' + worker_id + '/exec'
response = requests.post(url, headers=headers, json=json_data)

rd = response.json()
exec_id = rd["Id"]
print("Exec instance id: ", rd['Id'])

json_data = {}
response = requests.post('http://192.168.43.47:56789/v1.41/exec/' + str(exec_id) + '/start', headers=headers, json=json_data)
print(response.text)

# CURL TO PREPARE EXEC: 
# curl -X POST -H "Content-Type: application/json" -d '{"Cmd": ["/bin/ash", "./simul.sh"]}' http://192.168.43.47:56789/v1.41/containers/{container_name} or {container_id}/exec
# exec_id is the return value from the exec instance creation(above command)

# CURL TO EXEC PREVIOUSLY PREPARED EXEC INSTANCE(SHOULD BE INSTANTLY AFTER THE PREVIOU COMMAND)# curl --output - -X POST -H "Content-Type: application/json" -d '{}' http://192.168.43.47:56789/v1.41/exec/{exec_id}/start


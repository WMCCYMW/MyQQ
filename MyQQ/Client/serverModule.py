import socket
import MessageQueue
import json
IP=""
Port=""
ss=""
def Reciver(clientsocket):
    while True:
        response_json= str(clientsocket.recv(1024),encoding='utf-8')
        response=json.loads(response_json)
        MessageQueue.mq.put(response)



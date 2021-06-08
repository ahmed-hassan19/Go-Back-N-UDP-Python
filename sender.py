import sys
from socket import *
import random

# Constants
MSS           = 13
WINDOW_SIZE   = 4
TIME_OUT      = 2
BUFFER_SIZE   = 2048

# Get the server hostname and port as command line arguments
argv          = sys.argv
filename      = argv[1]
receiver_IP   = argv[2]
receiver_port = argv[3]


print('filename: {}'.format(filename))
print('receiver_IP : {}'.format(receiver_IP))
print('receiver_port : {}'.format(receiver_port))
print('MSS: {}'.format(MSS))
print('window_size: {}'.format(WINDOW_SIZE))
print('time_out: {}'.format(TIME_OUT))

packets = []

with open(filename) as f:
    text = f.read()

packet_index = [i for i in range(len(text)) if i % MSS == 0]

packets.append(str(0) + '\r\n' + str(len(packet_index)+1))
print(f"Splitted the file to {len(packets)} packets.")
packet_id = 1
for i in range(1, len(packet_index)):
    packet = text[packet_index[i-1]:packet_index[i]]
    packets.append(str(packet_id)+'\r\n' + packet)

    packet_id += 1

if len(text) % MSS != 0:
    last_backet = text[packet_index[-1]:]
    packets.append(str(packet_id)+'\r\n' + last_backet)

addr = (receiver_IP, int(receiver_port))
total_packets = len(packets)
window_start = 0
print("*"*40)
print("Starting server.")
print("*"*40)
sendertSocket = socket(AF_INET, SOCK_DGRAM)
sendertSocket.settimeout(TIME_OUT)
while True:
    window_end = min(window_start + WINDOW_SIZE, total_packets)
    print(f"Window starts from {window_start} to {window_end}.")
    for i in range(window_start, window_end):
        if random.randint(0, 10) > 2:
            sendertSocket.sendto(packets[i].encode(), addr)
        else:
            print(f"Packet {i} is lost.")
            print("*"*40)
    try:
        msg, addr = sendertSocket.recvfrom(BUFFER_SIZE)
        ack = int(msg.decode())
        # If acknowledgement for the last packet is recieved.
        if ack == total_packets - 1:
            sendertSocket.close()
            break
        if ack <= window_end:
            print(f"ACK {ack} recieved.")
            window_start = ack + 1
            print(f"Window now starts from {ack+1}.")
            print("*"*40)
    except OSError:
        print(f"Resending packets {window_start} to {window_end}.")
        print("*"*40)

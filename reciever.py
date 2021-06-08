import random
from socket import *
import sys
import os

# Constants
BUFFER_SIZE = 2048

# Get the server hostname and port as command line arguments
argv          = sys.argv
filename      = argv[1]
receiver_IP   = argv[2]
receiver_port = argv[3]

recieverSocket = socket(AF_INET, SOCK_DGRAM)
recieverSocket.bind((receiver_IP, int(receiver_port)))

file_data = []
recvd_base = 0
total_packets = None
print("Starting server.")
print("*"*40)
while True:
    # Wait until recieving the first packet.
    while recvd_base == 0:
        msg, addr = recieverSocket.recvfrom(BUFFER_SIZE)
        seq_num, data = msg.decode().split('\r\n')
        ack = int(seq_num)
        if ack == 0:
            print(f"Recieved first packet.")
            total_packets = int(data)
            print(f"Total number of packets: {total_packets}")
            print("*"*40)
            recvd_base += 1
            recieverSocket.sendto(str(ack).encode(), addr)
            break
    msg, addr = recieverSocket.recvfrom(BUFFER_SIZE)
    seq_num, data = msg.decode().split('\r\n')
    ack = int(seq_num)
    if ack == recvd_base:
        print(f"Recieved packet number {ack}.")
        print(f"Sending acknowledgement number {ack}.")
        print("*"*40)
        recvd_base += 1
        # Simulate ack loss
        if random.randint(0, 10) > 2:
            recieverSocket.sendto(str(ack).encode(), addr)
        else:
            print(f"Acknowledgement {ack} is lost.")
            print("*" * 40)
        file_data.append(data)
    if recvd_base == total_packets:
        print("Recieved all packets. Writing the data to a file.")
        recieverSocket.sendto(str(ack).encode(), addr)
        recieverSocket.close()
        with open(filename, 'w+') as f:
            f.write(''.join(file_data))
        print("Wrote data to the output file:")
        print(file_data)
        print("*"*40)
        break

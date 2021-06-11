import random
from socket import *
import sys
import os
import time


# Constants
BUFFER_SIZE = 2048

def reciev(filename,receiver_IP,receiver_port,MSS,WINDOW_SIZE,TIME_OUT):
        print('filename: {}'.format(filename))
        print('receiver_IP : {}'.format(receiver_IP))
        print('receiver_port : {}'.format(receiver_port))

        ADRR = (receiver_IP, int(receiver_port))
        recieverSocket = socket(AF_INET, SOCK_DGRAM)

        recieverSocket.bind(ADRR)

        file_data = []
        recvd_base = 0
        total_packets = None

        print(f"Server is listening on {ADRR}")
        print("*"*40)

        while True:
            # Wait until receiving the first packet.
            while recvd_base == 0:
                msg, addr = recieverSocket.recvfrom(BUFFER_SIZE)
                #Get the connection intial time
                inital_time = time.time()

                seq_num, data = msg.decode().split('\r\n')
                ack = int(seq_num)
                if ack == 0:
                    print(f"Received first packet.")
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
                    print("Continuing using the accumulated acknowledgements policy.")
                    print("*" * 40)
                file_data.append(data)
            if recvd_base == total_packets:
                print("Recieved all packets. Writing the data to a file.")
                recieverSocket.sendto(str(ack).encode(), addr)
                recieverSocket.close()
                with open(filename, 'w+') as f:
                    f.write(''.join(file_data))
                #Get the connection final time
                final_time = time.time()
                
                connection_time = final_time - inital_time
                transmission_rate =   total_packets / connection_time

                print("Wrote data to the output file:")
                print("*"*40)

                results = f"For experiment of {filename} with the following parameters: \n\
                {{\n\
                MSS: {MSS}\n\
                WINDOW_SIZE: {WINDOW_SIZE}\n\
                TIME_OUT: {TIME_OUT}\n\
                }}\n\
                It took {connection_time} secs to transmit {total_packets} packets with a transmission rate = {transmission_rate} packets/sec\
                \n"

                with open('EXPERIMENTS_RESULTS.txt', 'a') as f:
                    f.write(results)
                    f.write('*'*120 + '\n')
                break

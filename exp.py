import sender
import reciever
import threading
import time
import sys

# Constants
MSS           = 1400
WINDOW_SIZE   = 10
TIME_OUT      = 1
BUFFER_SIZE   = 2048

# Get the server hostname and port as command line arguments
argv          = sys.argv
file_name     = argv[1]
IP_adress     = argv[2]
port_number   = argv[3]

output_file_name = file_name[:-4] + '_output' + file_name[-4:]
print('================================================================')
print('Beginning of the reciver thread:')
print('=================================================================')

thread_recv = threading.Thread(target=reciever.reciev,
    args=(output_file_name, IP_adress, int(port_number), MSS, WINDOW_SIZE, TIME_OUT))

thread_recv.start()

time.sleep(1)

print('================================================================')
print('Begaining of sender thread')
print('=================================================================')

thread_send = threading.Thread(target=sender.send,
    args=(file_name, IP_adress, int(port_number), MSS, WINDOW_SIZE, TIME_OUT))

thread_send.start()
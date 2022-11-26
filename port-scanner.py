#!/usr/bin/python3

import sys
import socket
import time
from datetime import datetime
from threading import Thread

# FUNCTIONS
def error(message):
    print(message)
    print("Usage: ./scanner.py <target> <first port> <last port>")
    sys.exit()

def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((target, port))
        if result == 0:
            print(f"Port {port} is open")
        s.close

    except KeyboardInterrupt:
        print('\nExiting program.')

    except socket.gaierror:
        print(f"Hostname {target} couldn't be resolved.")

    except socket.error:
        # comment out because of too many error messages
        # print(f"Couldn't connect to {target}:{port}.")
        pass

#MAIN
# argument count
if len(sys.argv) < 2 or len(sys.argv) > 4:
    error("Invalid number of arguments.")

# get ip from
target = socket.gethostbyname(sys.argv[1])

# default ports and range
if sys.argv[2] != "" :
    first_port = int(sys.argv[2])
else:
    first_port = 1

if sys.argv[3] != "" :
    last_port = int(sys.argv[3])
else:
    last_port = 1000

# increase last_port by 1 because last value in range is skipped
last_port += 1

# Ensure port range is not exceeded
port_range_error = False
if first_port < 1:
    port_range_error = True
    first_port = 1
if last_port < 1:
    port_range_error = True
    last_port = 1
if first_port > 65536:
    port_range_error = True
    first_port = 65536
if last_port > 65536:
    port_range_error = True
    last_port = 65536
if port_range_error:
    print("Ports must in range of 1-65536")

if first_port > last_port:
    error("<first port> must be smaller or equal to <last port>")

# start banner
print('-' * 50)
print(f"Scanning:  {target}")
print(f"Timestamp: {datetime.now()}")
print('-' * 50)

# scanning routine with threads
start_time = int(time.time())
threads = {}

for port in range(first_port,last_port):
    threads[port] = Thread(target=scan_port, args=(port,), daemon=True)

for port in range(first_port,last_port):
    threads[port].start()

for port in range(first_port,last_port):
    threads[port].join()

duration = int(time.time()) - start_time

# finish banner
print('-' * 50)
print("Scan ended")
print(f"Needed time: {duration} s")
print('-' * 50)

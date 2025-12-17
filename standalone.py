import os
from threading import Thread
from time import sleep
import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # Just a way to get local IP
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

ip = get_local_ip()

def runserver():
    # Use Gunicorn to run Django instead of runserver
    os.system(f'gunicorn myproject.wsgi:application --bind {ip}:80')

def launchchrome():
    sleep(2)  # Give Gunicorn time to start
    os.system(f'start chrome http://{ip}:80')

# Run the server and launch Chrome in parallel
t1 = Thread(target=runserver)
t2 = Thread(target=launchchrome)

t1.start()
sleep(2)  # Give some time for Gunicorn to initialize
t2.start()
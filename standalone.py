import os
from threading import Thread
from time import sleep
import socket
from waitress import serve
from autoparts.wsgi import application  # Replace with your project name

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
    # Use Waitress to serve Django app
    serve(application, host='0.0.0.0', port=80)

def launchchrome():
    sleep(2)  # Give Waitress time to start
    os.system(f'start chrome http://{ip}')

# Run the server and launch Chrome in parallel
t1 = Thread(target=runserver)
t2 = Thread(target=launchchrome)

t1.start()
sleep(2)  # Give some time for Waitress to initialize
t2.start()
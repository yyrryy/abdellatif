import subprocess
import time
import signal
import sys
import socket
local_port = 80
remote_port = 8081
remote_user = "boxer"
remote_host = "167.71.77.64"

RESTART_DELAY = 5
process = None
running = True

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = 'localhost'
    finally:
        s.close()
    return ip

ip = get_local_ip()
def start_ssh_tunnel():
    global process

    cmd = [
        "ssh",
        "-R", f"{remote_port}:{ip}:{local_port}",
        f"{remote_user}@{remote_host}"
    ]

    print("Starting SSH reverse tunnel...")
    process = subprocess.Popen(cmd)
    print(f"Tunnel established: {remote_host}:{remote_port} -> {ip}:{local_port}")


def stop_tunnel():
    global process
    if process and process.poll() is None:
        print("Stopping SSH tunnel...")
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()


def handle_exit(signum, frame):
    global running
    print("Shutting down tunnel manager...")
    running = False
    stop_tunnel()
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)


def main():
    global process

    while running:
        start_ssh_tunnel()
        exit_code = process.wait()
        print(f"SSH exited (code {exit_code}), restarting in {RESTART_DELAY}s")
        time.sleep(RESTART_DELAY)


if __name__ == "__main__":
    main()

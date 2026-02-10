import subprocess
import time
import signal
import sys

SSH_CMD = [
    "ssh",
    "-N",
    "-o", "BatchMode=yes",
    "-o", "ServerAliveInterval=30",
    "-o", "ServerAliveCountMax=3",
    "-o", "ExitOnForwardFailure=yes",
    "-o", "TCPKeepAlive=yes",
    "-R", "8081:localhost:80",
    "boxer@167.71.77.64",
]

RESTART_DELAY = 5
process = None
running = True


def start_tunnel():
    global process
    print("Starting SSH tunnel...")
    process = subprocess.Popen(
        SSH_CMD,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )


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
    while running:
        start_tunnel()
        exit_code = process.wait()
        print(f"SSH exited (code {exit_code}), restarting in {RESTART_DELAY}s")
        time.sleep(RESTART_DELAY)


if __name__ == "__main__":
    main()
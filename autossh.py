import subprocess
import time
import signal
import sys
local_port = 80       # Local port for Waitress
remote_port = 8081      # Port on remote server
remote_user = "boxer"
remote_host = "167.71.77.64"
SSH_CMD = [
        "ssh",
        "-fN",  # Run in background, no remote command
        "-R", f"{remote_port}:{ip}:{local_port}",
        f"{remote_user}@{remote_host}"
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
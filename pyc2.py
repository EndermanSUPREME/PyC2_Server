import threading
import requests
import socket
import argparse
import random

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
        lhost = str(self.lhost)
        lport = int(self.lport)

    def GetLhost(self):
        return self.lhost
    def GetLport(self):
        return self.lport
    
def RunServer(ip):
    try:
        global serverIsRunning

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

        # Shutdown the Socket Server
        serversocket.close()
    except Exception as e:
        print(f"Error: {e}")

    print("[*] Server Session Ended!")

def main():# Create the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--lhost', type=str, help='Desired Listener IP [local / public / 0.0.0.0]')
    args = parser.parse_args()

    lhost = ""
    if len(vars(args)) > 0:
        lhost = args.lhost
    else:
        lhost = "local"

    # start server on a thread
    serverThread = threading.Thread(RunServer,args=[lhost])
    serverThread.start()

if __name__ == "__main__":
    main()
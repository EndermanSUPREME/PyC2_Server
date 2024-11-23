import threading
import socket
import json

class SessionData:
    def __init__(self, connection, address, session_exfil):
        self.connection = connection
        self.address = address
        self.session_os = session_exfil['os']
        self.session_name = session_exfil['user'] + "/" + self.GetAddress()

    def GetSessionOS(self):
        return self.session_os
    def GetSessionName(self):
        return self.session_name

    def GetConnection(self):
        return self.connection
    def GetAddress(self):
        return self.address

    def SetSessionOS(self, session_os):
        self.session_os = session_os
    def SetSessionName(self, session_name):
        self.session_name = session_name

class Session:
    def __init__(self, connection, address):
        # Server sends a message to the Client for a JSON
        # exfil of the environment (user and operating system)
        connection.sendall(b'exfil')
        exfilRecv = json.loads(connection.recv(1024).decode())

        # Set Object variables
        self.connection = connection
        self.session_data = SessionData(connection, address, exfilRecv)
        self.alive = True

    def GetSessionData(self):
        return self.session_data

    def EndSession(self):
        self.connection.close()

    def Active(self):
        return self.alive

def SessionHandle(sess):
    try:
        while sess.Active():
            # Get Feedback from the Server
            recvBuffer = sess.GetSessionData().GetConnection().recv(1024) # size of recv bytes we allow

            if sess.Active() == False:
                break

            if len(recvBuffer) > 0:
                print(recvBuffer.decode())

    except Exception as e:
        return None
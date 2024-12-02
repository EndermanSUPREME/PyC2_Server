import threading
import socket
import json

class SessionData:
    def __init__(self, connection, address, session_exfil: str):
        self.connection = connection
        self.address = address
        self.session_os = session_exfil['os']
        self.session_name = session_exfil['user']

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
    def __init__(self, connection, address, data: str):
        # Set Object variables
        self.connection = connection
        self.session_data = SessionData(connection, address, data)
        self.alive = True

    def GetSessionData(self):
        return self.session_data

    def EndSession(self):
        self.connection.close()

    def Active(self):
        return self.alive
import threading, socket, json, sys

class SessionData:
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address

    def GetConnection(self):
        return self.connection
    def GetAddress(self):
        return self.address

class Session:
    def __init__(self, connection, address):
        # Set Object variables
        self.connection = connection
        self.session_data = SessionData(connection, address)
        self.alive = True

    def TestConnection(self):
        self.session_data.GetConnection().settimeout(5)
        try:
            self.session_data.GetConnection().sendall(b'\n')
            output = self.session_data.GetConnection().recv(4096).decode()
            self.session_data.GetConnection().settimeout(None)
            return output
        except socket.timeout:
            self.session_data.GetConnection().settimeout(None)
            return str("")

    def GetSessionData(self):
        return self.session_data
    
    # send a command to session and print the returned buffer
    def SendCommand(self, payload:str=""):
        cmd = payload + "\n"
        sys.stdout.write("\b \b")
        sys.stdout.flush()

        self.GetSessionData().GetConnection().settimeout(None)
        try:
            self.GetSessionData().GetConnection().settimeout(5)
            # send over the command to the connection (session)
            self.GetSessionData().GetConnection().sendall(cmd.encode())
            try:
                ackID = 0
                while True:
                    # use a while-loop to ensure we capture everything
                    output = self.GetSessionData().GetConnection().recv(4096).decode()
                    if ackID == 0:
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                        sys.stdout.write(output[len(cmd):])
                    else:
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                        sys.stdout.write(output)
                    ackID = ackID + 1
            except socket.timeout:
                self.GetSessionData().GetConnection().settimeout(None)
        except Exception as e:
            print(f"Error: {e}")

    def EndSession(self):
        # send a kill command to the client so the
        # shell session gets terminated
        self.connection.send(b"exit\n")
        self.connection.close()

    def Active(self):
        return self.alive
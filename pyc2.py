import threading
import requests
import socket
import argparse
import random
import Server
import Prompt

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--lhost', type=str, help='Desired Listener IP [local / public / 0.0.0.0]')
    args = parser.parse_args()

    lhost = ""
    if len(vars(args)) > 0:
        lhost = args.lhost
    else:
        lhost = "local"

    # Start server on a thread
    serverThread = threading.Thread(Server.RunServer,args=[lhost])
    serverThread.start()

if __name__ == "__main__":
    main()
import threading, requests, socket, argparse, random
import Server, Prompt

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--lhost', type=str, help='Desired Listener IP [local / public / 0.0.0.0]')
    args = parser.parse_args()

    lhost = ""
    if len(vars(args)) > 1:
        lhost = args.lhost
    else:
        lhost = "local"

    lhost_lower = str(lhost).lower()

    # Set the configuration with an IP and random port
    print("Creating Server Config")
    MalServer = Server.ServerConfig(Server.GetIP(lhost_lower),random.randint(1024,65535))

    # Start server on a thread
    # print("Starting Mal-Server Thread")
    # serverThread = threading.Thread(target=Server.RunServer,args=[MalServer])
    # serverThread.start()

    # Start CLI thread
    print("Starting C2-CLI")
    commandHandler = Prompt.HandlerPrompt(MalServer)
    cliThread = threading.Thread(target=Prompt.ProcessCommand,args=[commandHandler])
    cliThread.start()

    cliThread.join()
    # serverThread.join()

if __name__ == "__main__":
    main()
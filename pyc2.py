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

    # Start CLI thread
    print("Starting C2-CLI")

    # Set the configuration with an IP and random port
    print("Creating Server Config")
    MalServer = Server.ServerConfig(Server.GetIP(lhost_lower),random.randint(4096,65535))

    commandHandler = Prompt.HandlerPrompt(MalServer)
    commandHandler.WriteToTerminal("Starting C2 Terminal Thread")
    cliThread = threading.Thread(target=Prompt.ProcessCommand,args=[commandHandler])
    cliThread.start()

    # Start server on a thread
    commandHandler.WriteToTerminal("Starting Mal-Server Thread")
    serverThread = threading.Thread(target=Server.RunServer,args=[MalServer,commandHandler])
    serverThread.start()

    cliThread.join()
    serverThread.join()

if __name__ == "__main__":
    main()
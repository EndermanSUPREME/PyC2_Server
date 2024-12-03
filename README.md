# PyC2

## Description
This project focuses on the basic idea and implementation of a C2 (Command and Control) Server using Python,
I created another project like this using [primarily C++](https://github.com/EndermanSUPREME/CPP_C2_Server). What is a C2 Server? A C2 is a tool that hackers
use to manage multiple compromised devices, for large operations this tool can be useful if the target size
is large. There are many widely used tools that perform the task of managing multiple compromised devices:
Meterpreter, HAVOC, Sliver, Colbalt Strike, Empire.

This project allows the user to host a socket-server on a random port, manipulate sessions, create executables
you can drop to get basic reverse shells against Windows and Linux targets. The C2 and Script interfaces have
there own set of commands, you can run `-h/--help` for a help-page.

## :wrench: Building PyC2
```bash
# Clone the repository
git clone https://github.com/EndermanSUPREME/PyC2_Server.git

# Move into the new directory and start up the server
cd PyC2_Server

# Install dependencies via pip
# NOTE: requires "pyinstaller" to be installed locally
pip install -r requirements.txt
```

## :desktop_computer: Running PyC2
Running the server is fairly simple, if no parameters are defined the server will be hosted locally
on the network you are connected to. The following argument can be one of the following: `local / public / 0.0.0.0`
the last option means you can provide an IP manually assuming it is pointing to yourself. This is to
allow multiple interfaces to be used, if for example you play HackTheBox they use interface tun0 for communication.

### Examples
`python3 pyc2.py`<br>
`python3 pyc2.py --lhost public`<br>
`python3 pyc2.py -l 10.10.14.45`

## Handling Sessions
While within the C2 interface (C2 >) when you capture a new session you will see a line of text print
to the screen notifying you about a new connection (IP,PORT).

*Note, the following commands assume you are on the C2 Interface*<br>
To view all captured sessions run `-s/--sessions`<br>
```text
=========== Sessions =============
Session ID  |    Session Details
------------+---------------------
0           | ('10.0.2.15', 60628)
------------+---------------------
1           | ('10.0.3.35', 34668)
------------+---------------------
2           | ('10.0.3.82', 24351)
==================================
```
To interact with a specific session run `-i/--interact [session id]`.<br>
To kill a specific session run `-k/--kill [session id]`.<br>
To kill all sessions run `-K/--kill-all`.

## Creating Droppers
While within the C2 interface (C2 >) you can transition to the Scripting interface (Script >) by entering `script`
once in the scripting interface you can create droppers targeted to Windows or Linux via `-t [target os]`.

A `malclient.py` is created locally and pyinstaller will compile this into binaries that can be
executed on your target os.

These executables will be located in your current working directory called
`malclient` (Unix) or `malclient.exe` (Windows)

```bash
┌──(daegon㉿UnDefinedCS)-[~/PyC2_Server]
└─$ python3 pyc2.py                                                                                                  
Starting C2-CLI
Creating Server Config
Getting LAN IP. . .
Starting C2 Terminal Thread
Starting Mal-Server Thread
[*] Attempting to Bind to >> 10.0.2.15:62790
[+] Server Active | 10.0.2.15:62790
C2 > script
Script > -t unix
[+] Created malclient.py
[*] Building portable executable. . .
pygame 2.5.2 (SDL 2.30.6, Python 3.12.6)
Hello from the pygame community. https://www.pygame.org/contribute.html
[*] Performing Clean-Up. . .
[+] Created malclient! (Unix Executable)
```

## Developer Notes
This project is not intended to be used for malicious purposes, please use all hacking tools responsibly and always have permission to attack a device.
The ScriptMaker feature is not designed to be used against hardened systems, Anti-Virus will flag all executables generated.
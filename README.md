# Villain Netcat

Villain Netcat Tool is a versatile Python-based network utility inspired by the traditional `netcat` tool. It provides a powerful set of features for penetration testing, network debugging, file transfers, and remote system management.

---

## Features

- **Command Shell Access**: Interact with a remote command-line interface.
- **File Uploading**: Upload files to a remote server over TCP.
- **Command Execution**: Execute system commands remotely and return output.
- **Interactive Communication**: Send and receive data interactively between client and server.
- **Listener Mode**: Act as a server to handle incoming client connections.
- **Client Mode**: Connect to a server for communication or file transfer.

---

## Requirements

- Python 3.x
- Admin/root privileges for binding to low-numbered ports (if required)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/naruto-net-tool.git

1. Nagitive to project derectory:
   ```bash
   cd villain-netcat

2. Run the tool directly using python:
   ```bash
   python netcat.py
---

## Examples:

1. Start a command shell on the target:
   ```bash
   python netcat.py -t 192.168.1.108 -p 5555 -l -c
   
2. Upload a file to the target:
   ```bash
   python netcat.py -t 192.168.1.108 -p 5555 -l -u=myfile.txt

3. Execute a command on the target:
   ```bash
   python netcat.py -t 192.168.1.108 -p 5555 -l -e="cat /etc/passwd"

4. Send data to a listening server:
   ```bash
   echo 'Hello World' | python netcat.py -t 192.168.1.108 -p 135

5. Connect to a remote server interactively:
   ```bash
   python netcat.py -t 192.168.1.108 -p 5555

---

## Disclaimer

This tool is intended for ethical hacking, penetration testing, and educational purposes only. Unauthorized use of this tool on networks or systems you do not own is illegal. Always obtain proper permissions before using this tool.

---

## Contributions

Contributions, issues, and feature requests are welcome! Feel free to fork the project and submit a pull request. 

---


## Contact

For any questions or suggestions, feel free to contact:

- Name: `Mohammad Tanvir`

- GitHub: [GitHub Profile](https://github.com/villainXtanvir/)

- Email: `villainxtanvir@gmail.com`

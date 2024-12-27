import argparse  # For parsing command-line arguments
import socket  # For network connections
import shlex  # For splitting shell-like command strings
import subprocess  # For executing system commands
import sys  # For system-specific functions and exit handling
import textwrap  # For formatting command-line text
import threading  # For running multiple threads concurrently

# Function to execute a system command and return its output
def execute(cmd):
    cmd = cmd.strip()  # Remove any extra spaces
    if not cmd:  # Return nothing if the command is empty
        return
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)  # Execute the command
    return output.decode()  # Return the output as a string

# NetCat class definition for network communication
class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args  # Command-line arguments
        self.buffer = buffer  # Initial buffer (data to send)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reuse of the address

    # Main method to decide between sending or listening
    def run(self):
        if self.args.listen:  # If in listen mode
            self.listen()
        else:  # If in send mode
            self.send()

    # Method to send data to a server
    def send(self):
        self.socket.connect((self.args.target, self.args.port))  # Connect to the target IP and port
        if self.buffer:  # If there is data in the buffer
            self.socket.send(self.buffer)  # Send the data
        try:
            while True:  # Loop to interact with the server
                recv_len = 1  # Track received data length
                response = ''
                while recv_len:  # While there is data to receive
                    data = self.socket.recv(4096)  # Receive up to 4096 bytes
                    recv_len = len(data)  # Update the received length
                    response = data.decode()  # Decode received data
                    if recv_len < 4096:  # If less than 4096 bytes were received, exit the loop
                        break
                if response:  # If there is a response
                    print(response)  # Print the server response
                    buffer = input("> ")  # Prompt for user input
                    buffer += "\n"  # Add a newline
                    self.socket.send(buffer.encode())  # Send the input
        except KeyboardInterrupt:  # Handle user interruption
            print("user terminated")
            self.socket.close()  # Close the socket
            sys.exit()  # Exit the program

    # Method to listen for incoming connections
    def listen(self):
        self.socket.bind((self.args.target, self.args.port))  # Bind to the target IP and port
        self.socket.listen(5)  # Start listening for connections (queue up to 5 connections)

        while True:  # Loop to handle multiple connections
            client_socket, _ = self.socket.accept()  # Accept an incoming connection
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))  # Create a thread to handle the client
            client_thread.start()  # Start the thread

    # Method to handle client connections
    def handle(self, client_socket):
        if self.args.execute:  # If execute option is set
            output = execute(self.args.execute)  # Execute the specified command
            client_socket.send(output.encode())  # Send the command output to the client
        elif self.args.upload:  # If upload option is set
            file_buffer = b''  # Create a buffer for the file
            while True:
                data = client_socket.recv(4096)  # Receive file data
                if data:
                    file_buffer += data  # Append received data to the buffer
                else:
                    break
            with open(self.args.upload, 'wb') as f:  # Write the buffer to a file
                f.write(file_buffer)
            message = f"Saved file {self.args.upload}"  # Confirmation message
            client_socket.send(message.encode())  # Send confirmation to the client
        elif self.args.command:  # If command shell option is set
            cmd_buffer = b''  # Buffer for the shell commands
            while True:
                try:
                    client_socket.send(b'BHP: #> ')  # Prompt for input
                    while '\n' not in cmd_buffer.decode():  # Wait for a complete command
                        cmd_buffer += client_socket.recv(64)  # Receive input from the client
                    response = execute(cmd_buffer.decode())  # Execute the command
                    if response:
                        client_socket.send(response.encode())  # Send the response to the client
                    cmd_buffer = b''  # Reset the buffer
                except Exception as e:  # Handle exceptions
                    print(f"Server killed {e}")
                    self.socket.close()  # Close the socket
                    sys.exit()  # Exit the program

# Main script execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Naruto Net Tool",  # Description of the tool
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:  # Examples of usage
            netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload to file
            netcat.py -t 192.168.1.108 -p 5555 -l -e="cat /etc/passwd" # execute command
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
            netcat.py -t 192.168.1.108 -p 5555 # Connect to server
        ''')
    )
    
    # Adding arguments for the parser
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified PORT')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    
    args = parser.parse_args()  # Parse command-line arguments
    
    if args.listen:  # Set the buffer based on the mode
        buffer = ''
    else:
        buffer = sys.stdin.read()  # Read input from stdin

    nc = NetCat(args, buffer.encode())  # Create a NetCat object with arguments and buffer
    nc.run()  # Run the NetCat object

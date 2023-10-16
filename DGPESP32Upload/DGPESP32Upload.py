import os
from collections.abc import Generator
import socket
from DGPESP32Control import DGPESP32Control

def __check_response(sock: socket.socket, success_prefix: str, failure_prefix: str) -> bool:
    msg = sock.recv(128).decode()
    if msg.startswith(success_prefix):
        return True
    if msg.startswith(failure_prefix):
        print(msg)
        return False
    return False

def __send_command(sock: socket.socket, cmd: str, success_prefix: str, failure_prefix: str) -> bool:
    sock.send(f'{cmd}\n'.encode())
    return __check_response(sock, success_prefix, failure_prefix)

def upload_file(file_path: str, address: int) -> Generator[int]:
    ip   = DGPESP32Control.ip()
    port = DGPESP32Control.port()

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))

        if not __send_command(sock, 'TEST', 'OK', 'NOK'):
            yield 0
            return

        size = os.stat(file_path).st_size
        if not __send_command(sock, f'TRANSFER {address} {size}', 'OK', 'NOK'):
            yield 0
            return
        
        with open(file_path, 'rb') as f:
            bytes_sent = 0
            while True:
                data = f.read(4096)
                if not data:
                    break
                sock.send(data)
                bytes_sent += len(data)
                yield bytes_sent

        if not __check_response(sock, 'TaskSucceeded', 'TaskFailed'):
            yield 0
            return
        
    except:
        return 0

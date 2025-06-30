import json
import os
import re
import socket
import subprocess

from dotenv import load_dotenv


def start_server(
    host: str = '127.0.0.1',
    port: int = 4000,
    allowed_origin: str = '*'
):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((host, port))
            sock.listen()
            print(f'TCP server listening on {host}:{port}')
            while True:
                conn, addr = sock.accept()
                print(f'{addr} connected')

                if allowed_origin and allowed_origin != '*'\
                        and not re.match(allowed_origin, addr):
                    conn.close()
                    continue

                # Set message timeout
                conn.settimeout(2)
                with conn:
                    try:
                        data, addr = conn.recvfrom(1024)
                        data = data.decode('utf-8').strip().lower()
                        match data:
                            case 'shutdown':
                                conn.sendall(json.dumps(
                                    {'status': 200, 'msg': 'ok'}).encode('utf-8'))
                                conn.close()
                                sock.close()
                                print('Shutting down system')
                                subprocess.call(['shutdown', '-h', 'now'])
                        conn.sendall(json.dumps(
                            {'status': 200, 'msg': 'ok'}).encode('utf-8'))
                    except TimeoutError:
                        conn.sendall(json.dumps(
                            {'status': 408, 'msg': 'timeout'}).encode('utf-8'))
                    conn.close()
            sock.close()
    except KeyboardInterrupt:
        print('TCP server stoppped')


def main():
    load_dotenv()
    host = os.getenv('SERVER_HOST')
    port = os.getenv('SERVER_PORT')
    allowed_origin = os.getenv('ALLOWED_ORIGIN')

    start_server(host=host if host else '127.0.0.1',
                 port=int(port) if port else 4000,
                 allowed_origin=allowed_origin if allowed_origin else '*')


main()

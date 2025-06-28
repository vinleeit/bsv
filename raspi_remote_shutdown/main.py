import socket
import json
import subprocess

HOST = '127.0.0.1'
PORT = 2225

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        print(f'TCP server listening on {HOST}:{PORT}')
        while True:
            conn, addr = sock.accept()
            print(f'{addr} connected')

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

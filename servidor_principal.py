import socket
import json
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def send_to_operation_server(host, port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.send(json.dumps(data).encode())
        result = json.loads(s.recv(4096).decode())
    return result

def main():
    host = '192.168.56.2'  # Dirección IP del servidor principal
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Servidor principal escuchando en {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Conexión establecida desde {addr}")

        data = conn.recv(4096).decode()
        matrices = json.loads(data)

        N = matrices['N']
        matrix_a = matrices['matrix_a']
        matrix_b = matrices['matrix_b']

        # Dividir la matriz A en dos partes
        mid = N // 2
        a1, a2 = matrix_a[:mid], matrix_a[mid:]

        # Preparar datos para los servidores de operación
        data1 = {'a': a1, 'b': matrix_b}
        data2 = {'a': a2, 'b': matrix_b}

        # Enviar tareas a los servidores de operación de forma asíncrona
        with ThreadPoolExecutor(max_workers=2) as executor:
            future1 = executor.submit(send_to_operation_server, '192.168.56.3', 5001, data1)
            future2 = executor.submit(send_to_operation_server, '192.168.56.4', 5002, data2)

            result1 = future1.result()
            result2 = future2.result()

        # Combinar resultados
        final_result = result1 + result2

        conn.send(json.dumps(final_result).encode())
        conn.close()

if __name__ == "__main__":
    main()
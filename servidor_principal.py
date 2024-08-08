import socket
import json
import numpy as np
from concurrent.futures import ThreadPoolExecutor

def send_to_operation_server(host, port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(json.dumps(data).encode(), (host, port))
        result, _ = s.recvfrom(4096)
    return json.loads(result.decode())

def main():
    host = '192.168.56.2'  # Dirección IP del servidor principal
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print(f"Servidor principal escuchando en {host}:{port}")

    while True:
        data, addr = server_socket.recvfrom(4096)
        print(f"Datos recibidos de {addr}")

        matrices = json.loads(data.decode())

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

        # Enviar el resultado de vuelta al cliente
        server_socket.sendto(json.dumps(final_result).encode(), addr)

if __name__ == "__main__":
    main()

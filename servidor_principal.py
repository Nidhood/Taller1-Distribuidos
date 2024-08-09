import socket
import json
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

def send_to_operation_server(host, port, data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.send(json.dumps(data).encode())
            result = json.loads(s.recv(4096).decode())
        return result
    except Exception as e:
        print(f"Error al conectar con el servidor {host}:{port} - {e}")
        return None

def main():
    host = '127.0.0.1'  # Dirección IP del servidor principal 192.168.56.2
    port = 5004

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Servidor principal escuchando en {host}:{port}/TCP")

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
            futures = {
                executor.submit(send_to_operation_server, host, 5001, data1): 'data1',
                executor.submit(send_to_operation_server, host, 5002, data2): 'data2'
            }

            results = {}
            for future in as_completed(futures):
                result = future.result()
                if result is not None:
                    results[futures[future]] = result

            # Si uno de los servidores falla, reasignar la tarea al otro servidor
            if 'data1' not in results:
                results['data1'] = send_to_operation_server(host, 5002, data1)
            if 'data2' not in results:
                results['data2'] = send_to_operation_server(host, 5001, data2)

        # Combinar resultados
        final_result = results['data1'] + results['data2']

        conn.send(json.dumps(final_result).encode())
        conn.close()

if __name__ == "__main__":
    main()

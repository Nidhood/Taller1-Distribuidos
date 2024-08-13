import socket
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

def send_to_operation_server(host, port, data, num):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.send(json.dumps(data).encode())
            result = json.loads(s.recv(4096).decode())
        return result
    except Exception as e:
        print(f"Error al conectar con el servidor de operación {num} {host}:{port} - {e}")
        return None

def main():
    host = '127.0.0.1'  # Dirección IP del servidor principal 192.168.56.2
    port = 5004         # Puerto libre para la conexión con el servidor principal

    # Lógica para abrir las conexiones con el servidor principal
    print("Iniciando servidor principal")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Servidor principal escuchando en {host}:{port}/TCP")

    # Lógica para recibir las matrices y dividirlas
    while True:
        print("Esperando conexión de cliente...")
        conn, addr = server_socket.accept()
        print(f"Conexión establecida desde {addr}")
        data = conn.recv(4096).decode()
        print("Datos recibidos del cliente")
        matrices = json.loads(data)
        N = matrices['N']
        matrix_a = matrices['matrix_a']
        matrix_b = matrices['matrix_b']

        # Dividir la matriz A en dos partes:
        mid = N // 2
        a1, a2 = matrix_a[:mid], matrix_a[mid:]

        # Dividir la matriz B en dos partes:
        b1, b2 = matrix_b[:mid], matrix_b[mid:]

        # Preparar datos para los servidores de operación
        data1 = {'a': a1, 'b': b1}
        data2 = {'a': a2, 'b': b2}

        # Enviar tareas a los servidores de operación de forma asíncrona
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {
                executor.submit(send_to_operation_server, host, 5001, data1, 1): 'data1',
                executor.submit(send_to_operation_server, host, 5002, data2, 2): 'data2'
            }

            results = {}
            for future in as_completed(futures):
                data_key = futures[future]
                result = future.result()
                if result is not None:
                    results[data_key] = result
                    print(f"Resultado recibido para {data_key}")
                else:
                    print(f"Fallo en el cálculo de {data_key}")

            if 'data1' not in results:
                print("Reasignando cálculo de data1 al servidor 5002")
                results['data1'] = send_to_operation_server(host, 5002, data1, 1)
                print("Resultado recibido para data1")
            if 'data2' not in results:
                print("Reasignando cálculo de data2 al servidor 5001")
                results['data2'] = send_to_operation_server(host, 5001, data2, 2)
                print("Resultado recibido para data2")

        # Combinar resultados
        final_result = results['data1'] + results['data2']
        print("Enviando resultado final al cliente")
        conn.send(json.dumps(final_result).encode())
        conn.close()
        print("Conexión con el cliente cerrada")

if __name__ == "__main__":
    main()

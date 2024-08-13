import socket
import json
import numpy as np

def print_matrix(matrix, name):
    print(f"\nMatriz {name}:")
    for row in matrix:
        print([round(x, 2) for x in row])

def main():
    host = '127.0.0.1'  # Dirección IP del servidor de operación 2  192.168.56.4
    port = 5002         # Puerto libre para la conexión con el servidor de operación 2

    # Lógica para abrir las conexiones con el servidor de operación 2
    print("Iniciando servidor de operación 2")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Escuchando en {host}:{port}/TCP")

    # Lógica para recibir las matrices y multiplicarlas
    while True:
        print("Esperando conexión del servidor principal...")
        conn, addr = server_socket.accept()
        print(f"Conexión establecida desde {addr}")

        try:
            data = conn.recv(4096).decode()
            print("Datos recibidos del servidor principal")
            matrices = json.loads(data)

            print("Realizando multiplicación de matrices")
            result = np.multiply(matrices['a'], matrices['b']).tolist()

            print_matrix(matrices['a'], "A")
            print_matrix(matrices['b'], "B")
            print_matrix(result, "Resultado")

            print("Enviando resultado al servidor principal")
            conn.send(json.dumps(result).encode())
            print("Resultado enviado exitosamente")

        except Exception as e:
            print(f"Error inesperado: {e}")
        finally:
            conn.close()
            print("Conexión cerrada")

if __name__ == "__main__":
    main()
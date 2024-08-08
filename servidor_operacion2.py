import socket
import json
import numpy as np

def multiply_matrices(a, b):
    return np.dot(a, b).tolist()

def main():
    host = '192.168.56.4'  # Cambia según el servidor
    port = 5002  # Puerto correspondiente al servidor

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print(f"Servidor de operación escuchando en {host}:{port}")

    while True:
        data, addr = server_socket.recvfrom(4096)
        print(f"Conexión establecida desde {addr}")

        matrices = json.loads(data.decode())

        result = multiply_matrices(matrices['a'], matrices['b'])

        # Enviar el resultado de vuelta al servidor principal
        server_socket.sendto(json.dumps(result).encode(), addr)

if __name__ == "__main__":
    main()

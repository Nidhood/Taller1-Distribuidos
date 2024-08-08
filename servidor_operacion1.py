import socket
import json
import numpy as np

def multiply_matrices(a, b):
    return np.dot(a, b).tolist()

def print_matrices_side_by_side(matrix_a, matrix_b, result):
    max_rows = max(len(matrix_a), len(matrix_b), len(result))

    print("Matriz A".ljust(20), "Matriz B".ljust(20), "Resultado")
    print("=" * 60)

    for i in range(max_rows):
        # Imprimir fila de Matriz A
        if i < len(matrix_a):
            print(" | ".join([f"{round(x, 2):7}" for x in matrix_a[i]]), end="")
        else:
            print(" " * (len(matrix_a[0]) * 8), end="")

        print("    ", end="")  # Espacio entre matrices

        # Imprimir fila de Matriz B
        if i < len(matrix_b):
            print(" | ".join([f"{round(x, 2):7}" for x in matrix_b[i]]), end="")
        else:
            print(" " * (len(matrix_b[0]) * 8), end="")

        print("    ", end="")  # Espacio entre matrices

        # Imprimir fila del Resultado
        if i < len(result):
            print(" | ".join([f"{round(x, 2):7}" for x in result[i]]))
        else:
            print("")

def main():
    host = '192.168.56.3'  # Dirección IP del servidor de operación 1
    port = 5001

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Servidor de operacion 1 escuchando en {host}:{port}/TCP")

    while True:
        conn, addr = server_socket.accept()
        print(f"Conexión establecida desde {addr}")

        data = conn.recv(4096).decode()
        matrices = json.loads(data)
        result = multiply_matrices(matrices['a'], matrices['b'])

        # Mostrar el proceso de multiplicación de matrices:
        print_matrices_side_by_side(matrices['a'], matrices['b'], result)

        # Enviar el resultado al servidor principal:
        conn.send(json.dumps(result).encode())

        conn.close()

if __name__ == "__main__":
    main()
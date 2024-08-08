import socket
import json
import numpy as np

def multiply_matrices(a, b):
    return np.dot(a, b).tolist()

def print_matrices_vertically(matrix_a, matrix_b, result):
    max_rows = max(len(matrix_a), len(matrix_b), len(result))
    max_cols_a = max(len(row) for row in matrix_a) if matrix_a else 0
    max_cols_b = max(len(row) for row in matrix_b) if matrix_b else 0
    max_cols_r = max(len(row) for row in result) if result else 0

    # Header
    print("Matriz A".ljust(max_cols_a * 8 + 4), end="")
    print("Matriz B".ljust(max_cols_b * 8 + 4), end="")
    print("Resultado".ljust(max_cols_r * 8 + 4))
    print("=" * (max_cols_a * 8 + max_cols_b * 8 + max_cols_r * 8 + 12))

    # Print matrices
    for i in range(max_rows):
        # Print row of Matriz A
        if i < len(matrix_a):
            row_a = " | ".join([f"{round(x, 2):7}" for x in matrix_a[i]])
        else:
            row_a = " " * (max_cols_a * 8)

        # Print row of Matriz B
        if i < len(matrix_b):
            row_b = " | ".join([f"{round(x, 2):7}" for x in matrix_b[i]])
        else:
            row_b = " " * (max_cols_b * 8)

        # Print row of Resultado
        if i < len(result):
            row_r = " | ".join([f"{round(x, 2):7}" for x in result[i]])
        else:
            row_r = " " * (max_cols_r * 8)

        # Print all rows
        print(row_a.ljust(max_cols_a * 8 + 4), end="")
        print(row_b.ljust(max_cols_b * 8 + 4), end="")
        print(row_r)

def main():
    host = '192.168.56.4'  # Dirección IP del servidor de operación 2
    port = 5002

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Servidor de operacion 2 escuchando en {host}:{port}/TCP")

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
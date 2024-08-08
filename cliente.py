import socket
import json

def main():
    host = '192.168.1.100'  # Dirección IP del servidor principal
    port = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Parámetros de entrada
    N = int(input("Ingrese la dimensión de las matrices: "))

    # Crear matrices de ejemplo (puedes modificar esto para ingresar matrices manualmente)
    matrix_a = [[i * 1.1 for i in range(N)] for _ in range(N)]
    matrix_b = [[i * 2.2 for i in range(N)] for _ in range(N)]

    data = {
        'N': N,
        'matrix_a': matrix_a,
        'matrix_b': matrix_b
    }

    client_socket.send(json.dumps(data).encode())

    result = client_socket.recv(4096).decode()
    print("Resultado de la multiplicación de matrices:")
    print(result)

    client_socket.close()


if __name__ == "__main__":
    main()
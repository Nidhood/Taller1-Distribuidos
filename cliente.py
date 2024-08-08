import socket
import json

def main():
    host = '192.168.52.2'  # Dirección IP del servidor principal
    port = 5000


    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Crear socket cliente con UDP
    client_socket.connect((host, port)) # Conectar al servidor principal

    # Parámetros de entrada
    N = int(input("Ingrese la dimensión de las matrices: "))

    # Crear matrices de ejemplo (puedes modificar esto para ingresar matrices manualmente)
    matrix_a = [[i * 1.1 for i in range(N)] for _ in range(N)]
    matrix_b = [[i * 2.2 for i in range(N)] for _ in range(N)]

    # Armar los datos a enviar
    data = {
        'N': N,
        'matrix_a': matrix_a,
        'matrix_b': matrix_b
    }

    # Enviar datos al servidor principal
    client_socket.send(json.dumps(data).encode())

    # Recibir el resultado
    result = client_socket.recv(4096).decode()
    print("Resultado de la multiplicación de matrices:")
    print(result)

    client_socket.close()


if __name__ == "__main__":
    main()
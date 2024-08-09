import socket
import json

def main():
    host = '127.0.0.1'  # Dirección IP del servidor principal 192.168.56.2
    port = 5000


    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port)) # Conectar al servidor principal

    # Parámetros de entrada
    N = int(input("Ingrese la dimensión de las matrices: "))

    # Crear matrices de ejemplo
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

    # Imprimir el resultado, con solo 2 decimales:
    for row in json.loads(result):
        print([round(x, 2) for x in row])

    client_socket.close()


if __name__ == "__main__":
    main()
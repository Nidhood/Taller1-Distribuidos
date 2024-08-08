import socket
import json

def main():
    host = '192.168.52.2'  # Dirección IP del servidor principal
    port = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Cambiar a UDP

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
    client_socket.sendto(json.dumps(data).encode(), (host, port))

    # Recibir el resultado
    result, _ = client_socket.recvfrom(4096)
    print("Resultado de la multiplicación de matrices:")
    print(result.decode())

    client_socket.close()

if __name__ == "__main__":
    main()

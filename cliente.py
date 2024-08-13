import socket
import json
import time

start_time = time.time()

def print_matrix(matrix, name):
    print(f"\nMatriz {name}:")
    for row in matrix:
        print([round(x, 2) for x in row])

def main():
    host = '127.0.0.1'  # Dirección IP del servidor principal
    port = 5004         # Puerto libre para la conexión con el servidor principal

    # Lógica para conectar al servidor:
    print("Iniciando cliente para multiplicación de matrices...")
    print(f"Intentando conectar al servidor en {host}:{port}")
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print("Conexión exitosa al servidor.")
    except ConnectionRefusedError:
        print("Error: No se pudo conectar al servidor. Asegúrese de que el servidor esté en ejecución.")
        return
    except Exception as e:
        print(f"Error inesperado al conectar: {e}")
        return

    # Logica para ingresar la dimensión de las matrices:
    while True:
        try:
            N = int(input("\nIngrese la dimensión de las matrices (N): "))
            if N > 0:
                break
            else:
                print("Por favor, ingrese un número positivo.")
        except ValueError:
            print("Por favor, ingrese un número entero válido.")
    print(f"Creando matrices de {N}x{N}...")

    # Creamos matriz A de ejemplo, con valores de 0 a N-1 en cada fila
    matrix_a = [[i for i in range(N)] for j in range(N)]
    print_matrix(matrix_a, "A")

    # Creamos matriz B de ejemplo, con valores múltiplos de 5
    matrix_b = [[(i * 5 + j * 5) for i in range(N)] for j in range(N)]
    print_matrix(matrix_b, "B")

    # Armar los datos a enviar
    data = {
        'N': N,
        'matrix_a': matrix_a,
        'matrix_b': matrix_b
    }
    print("Enviando datos al servidor...")
    client_socket.send(json.dumps(data).encode())
    print("Esperando respuesta del servidor...")
    result = client_socket.recv(4096).decode()

    # Lógica para mostrar el resultado:
    print(f"Respuesta recibida.")
    print("Resultado de la multiplicación de matrices:")
    result_matrix = json.loads(result)
    print_matrix(result_matrix, "Resultado")

    # Cerrar la conexión:
    client_socket.close()
    print("Conexión cerrada. Operación completada.")

if __name__ == "__main__":
    main()
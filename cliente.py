import grpc
import json
import time
import matrix_multiplication_pb2
import matrix_multiplication_pb2_grpc

start_time = time.time()


def print_matrix(matrix, name):
    print(f"\nMatriz {name}:")
    for row in matrix:
        print([round(x, 2) for x in row])


def main():
    host = '127.0.0.1'
    port = 5004

    print("Iniciando cliente para multiplicación de matrices...")
    print(f"Intentando conectar al servidor en {host}:{port}")
    try:
        with grpc.insecure_channel(f'{host}:{port}') as channel:
            stub = matrix_multiplication_pb2_grpc.MatrixMultiplicationStub(channel)
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

            matrix_a = [[i + j for i in range(N)] for j in range(N)]
            print_matrix(matrix_a, "A")

            matrix_b = [[(i * 5 + j * 5) for i in range(N)] for j in range(N)]
            print_matrix(matrix_b, "B")



            print("Enviando datos al servidor...")
            response = stub.Multiply(matrix_multiplication_pb2.MatrixPair(
                matrix_a=[item for sublist in matrix_a for item in sublist],
                matrix_b=[item for sublist in matrix_b for item in sublist],
                size=N
            ))
            result_matrix = response.result

            # Convertir la lista plana a una matriz 2D
            result_matrix_2d = [result_matrix[i * N:(i + 1) * N] for i in range(N)]

            print(f"Respuesta recibida.")
            print("Resultado de la multiplicación de matrices:")
            print_matrix(result_matrix_2d, "Resultado")

    except grpc.RpcError as e:
        print(f"Error al conectar con el servidor: {e}")


if __name__ == "__main__":
    main()

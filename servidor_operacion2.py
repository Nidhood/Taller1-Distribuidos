import grpc
from concurrent import futures
import numpy as np
import matrix_multiplication_pb2
import matrix_multiplication_pb2_grpc


def print_matrix(matrix, name):
    print(f"\nMatriz {name}:")
    for row in matrix:
        print([float(round(x, 2)) for x in row])

class MatrixMultiplicationServicer(matrix_multiplication_pb2_grpc.MatrixMultiplicationServicer):
    def Multiply(self, request, context):
        print(f"Servidor Operacion 2: Datos recibidos del servidor principal en {context.peer()}.")
        size = request.size
        matrix_a = np.array(request.matrix_a)
        matrix_b = np.array(request.matrix_b)

        rows_a = len(matrix_a) // size
        rows_b = len(matrix_b) // size

        try:
            matrix_a = matrix_a.reshape(rows_a, size)
            matrix_b = matrix_b.reshape(rows_b, size)
        except ValueError as e:
            context.set_code(grpc.StatusCode.UNKNOWN)
            context.set_details(f'Exception calling application: {e}')
            return matrix_multiplication_pb2.MatrixResult(result=[])

        print("Servidor Operacion 2: Realizando multiplicación de matrices...")
        result = np.multiply(matrix_a, matrix_b)

        print_matrix(matrix_a, "A")
        print_matrix(matrix_b, "B")
        print_matrix(result, "Resultado")

        result_flat = result.flatten().tolist()
        print("\nServidor Operacion 2: Enviando resultado al servidor principal...")
        print("Servidor Operacion 2: Resultado enviado exitosamente.")
        print("\n\n********************************\n\n")
        print("Servidor Operacion 2: Iniciando servidor de operación 2")
        print("Servidor Operacion 2: Escuchando en 127.0.0.1:5002/TCP")
        print("Servidor Operacion 2: Esperando conexión del servidor principal...")
        return matrix_multiplication_pb2.MatrixResult(result=result_flat)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    matrix_multiplication_pb2_grpc.add_MatrixMultiplicationServicer_to_server(MatrixMultiplicationServicer(), server)
    server.add_insecure_port('[::]:5002')
    print("\n\n********************************\n\n")
    print("Servidor Operacion 2: Iniciando servidor de operación 2")
    print("Servidor Operacion 2: Escuchando en 127.0.0.1:5002/TCP")
    server.start()
    print("Servidor Operacion 2: Esperando conexión del servidor principal...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

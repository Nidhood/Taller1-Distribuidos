import grpc
from concurrent import futures
import numpy as np
import matrix_multiplication_pb2
import matrix_multiplication_pb2_grpc

class MatrixMultiplicationServicer(matrix_multiplication_pb2_grpc.MatrixMultiplicationServicer):
    def Multiply(self, request, context):
        print("\n\n ******************************** \n\n")
        print("Servidor Operación 2: Recibida solicitud de multiplicación")
        size = request.size
        matrix_a = np.array(request.matrix_a)
        matrix_b = np.array(request.matrix_b)

        print(f"Matrix A: {matrix_a}")
        print(f"Matrix B: {matrix_b}")

        rows_a = len(matrix_a) // size
        rows_b = len(matrix_b) // size

        print(f"Matrix A size: {matrix_a.size}, expected shape: ({rows_a}, {size})")
        print(f"Matrix B size: {matrix_b.size}, expected shape: ({rows_b}, {size})")

        try:
            matrix_a = matrix_a.reshape(rows_a, size)
            matrix_b = matrix_b.reshape(rows_b, size)

        except ValueError as e:
            context.set_code(grpc.StatusCode.UNKNOWN)
            context.set_details(f'Exception calling application: {e}')
            return matrix_multiplication_pb2.MatrixResult(result=[])

        result = np.multiply(matrix_a, matrix_b).flatten().tolist()
        print(f"Matrix Resultado: {result}")
        print("Servidor Operación 2: Devolviendo resultado")
        return matrix_multiplication_pb2.MatrixResult(result=result)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    matrix_multiplication_pb2_grpc.add_MatrixMultiplicationServicer_to_server(MatrixMultiplicationServicer(), server)
    server.add_insecure_port('[::]:5002')
    print("Servidor Operación 2: Iniciando servidor en el puerto 5002")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
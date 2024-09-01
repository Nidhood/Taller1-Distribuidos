import grpc
from concurrent.futures import ThreadPoolExecutor, as_completed
import matrix_multiplication_pb2
import matrix_multiplication_pb2_grpc


class MatrixMultiplicationServicer(matrix_multiplication_pb2_grpc.MatrixMultiplicationServicer):

    def Multiply(self, request, context):
        print("\n\n ******************************** \n\n")
        print("Servidor Principal: Recibida solicitud de multiplicación")
        size = request.size
        matrix_a = request.matrix_a
        matrix_b = request.matrix_b

        print(f"Servidor Principal: Tamaño de la matriz: {size}")
        print(f"Datos enviados al servidor (matriz A): {matrix_a}")
        print(f"Datos enviados al servidor (matriz B): {matrix_b}")

        # Dividir la matriz A en dos partes:
        mid = size * size // 2
        a1, a2 = matrix_a[:mid], matrix_a[mid:]

        # Dividir la matriz B en dos partes:
        b1, b2 = matrix_b[:mid], matrix_b[mid:]

        print(f"Servidor Principal: Tamaño de la matriz A1: {len(a1)}, B1: {len(b1)}")
        print(f"Servidor Principal: Tamaño de la matriz A2: {len(a2)}, B2: {len(b2)}")

        data1 = {'a': a1, 'b': b1}
        data2 = {'a': a2, 'b': b2}

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {
                executor.submit(self.send_to_operation_server, '127.0.0.1', 5001, data1, size): 'data1',
                executor.submit(self.send_to_operation_server, '127.0.0.1', 5002, data2, size): 'data2'
            }

            results = {}
            for future in as_completed(futures):
                data_key = futures[future]
                result = future.result()
                if result is not None:
                    results[data_key] = result

            if 'data1' not in results:
                print("Servidor Principal: Reintentando data1 en el servidor 5002")
                results['data1'] = self.send_to_operation_server('127.0.0.1', 5002, data1, size)
            if 'data2' not in results:
                print("Servidor Principal: Reintentando data2 en el servidor 5001")
                results['data2'] = self.send_to_operation_server('127.0.0.1', 5001, data2, size)
            if results.get('data1') is None or results.get('data2') is None:
                context.set_code(grpc.StatusCode.UNKNOWN)
                context.set_details('No se pudieron obtener resultados de los servidores de operación')
                print("Servidor Principal: No se pudieron obtener resultados de los servidores de operación")
                return matrix_multiplication_pb2.MatrixResult(result=[])

        print("Servidor Principal: Combinando resultados")

        # Convert results to integers if they are floats
        results['data1'] = [int(x) for x in results['data1']]
        results['data2'] = [int(x) for x in results['data2']]

        print(f"Datos recibidos al servidor (matriz R1): {results.get('data1')}")
        print(f"Datos recibidos al servidor (matriz R2): {results.get('data2')}")

        final_result = results['data1'] + results['data2']

        print("Servidor Principal: Devolviendo resultado final")
        return matrix_multiplication_pb2.MatrixResult(result=final_result)

    def send_to_operation_server(self, host, port, data, size):
        try:
            with grpc.insecure_channel(f'{host}:{port}') as channel:
                stub = matrix_multiplication_pb2_grpc.MatrixMultiplicationStub(channel)
                response = stub.Multiply(matrix_multiplication_pb2.MatrixPair(
                    matrix_a=data['a'],
                    matrix_b=data['b'],
                    size=size
                ))
            return response.result
        except Exception as e:
            print(f"Error al conectar con el servidor {host}:{port} - {e}")
            return None


def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    matrix_multiplication_pb2_grpc.add_MatrixMultiplicationServicer_to_server(MatrixMultiplicationServicer(), server)
    server.add_insecure_port('[::]:5004')
    print("Servidor Principal: Iniciando servidor en el puerto 5004")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

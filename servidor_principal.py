import grpc
from concurrent.futures import ThreadPoolExecutor, as_completed
import matrix_multiplication_pb2
import matrix_multiplication_pb2_grpc

class MatrixMultiplicationServicer(matrix_multiplication_pb2_grpc.MatrixMultiplicationServicer):

    def Multiply(self, request, context):
        print(f"Conexión establecida desde {context.peer()}")
        print("Datos recibidos del cliente")
        size = request.size
        matrix_a = request.matrix_a
        matrix_b = request.matrix_b

        # Dividir la matriz A por filas:
        rows_a1 = (size + 1) // 2
        rows_a2 = size // 2

        a1 = matrix_a[:rows_a1 * size]
        a2 = matrix_a[rows_a1 * size:]

        # Dividir la matriz B por filas:
        b1 = matrix_b[:rows_a1 * size]
        b2 = matrix_b[rows_a1 * size:]

        data1 = {'a': a1, 'b': b1}
        data2 = {'a': a2, 'b': b2}

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {
                executor.submit(self.send_to_operation_server, '127.0.0.1', 5001, data1, size, 1): 'data1',
                executor.submit(self.send_to_operation_server, '127.0.0.1', 5002, data2, size, 2): 'data2'
            }

            results = {}
            for future in as_completed(futures):
                data_key = futures[future]
                result = future.result()
                if result is not None:
                    results[data_key] = result
                    print(f"Resultado recibido para {data_key}")
                else:
                    print(f"Fallo en el cálculo de {data_key}")

            if 'data1' not in results:
                print("Reasignando cálculo de data1 al servidor 5002")
                results['data1'] = self.send_to_operation_server('127.0.0.1', 5002, data1, size, 1)
                print("Resultado recibido para data1")
            if 'data2' not in results:
                print("Reasignando cálculo de data2 al servidor 5001")
                results['data2'] = self.send_to_operation_server('127.0.0.1', 5001, data2, size, 2)
                print("Resultado recibido para data2")
            if results.get('data1') is None or results.get('data2') is None:
                context.set_code(grpc.StatusCode.UNKNOWN)
                context.set_details('No se pudieron obtener resultados de los servidores de operación')
                print("No se pudieron obtener resultados de los servidores de operación")
                return matrix_multiplication_pb2.MatrixResult(result=[])

        print("Enviando resultado final al cliente...")
        print("Conexión cerrada exitosamente.")

        # Convert results to integers if they are floats
        results['data1'] = [int(x) for x in results['data1']]
        results['data2'] = [int(x) for x in results['data2']]

        final_result = results['data1'] + results['data2']
        print("\n\n******************************** \n\n")
        print("Iniciando servidor principal")
        print("Servidor principal escuchando en 127.0.0.1:5004/TCP")
        print("Esperando conexión con el cliente...")

        return matrix_multiplication_pb2.MatrixResult(result=final_result)

    def send_to_operation_server(self, host, port, data, size, num):
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
            print(f"Error al conectar con el servidor de operación {num} {host}:{port}")
            return None

def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    matrix_multiplication_pb2_grpc.add_MatrixMultiplicationServicer_to_server(MatrixMultiplicationServicer(), server)
    server.add_insecure_port('[::]:5004')
    print("\n\n******************************** \n\n")
    print("Iniciando servidor principal")
    print("Servidor principal escuchando en 127.0.0.1:5004/TCP")
    print("Esperando conexión con el cliente...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
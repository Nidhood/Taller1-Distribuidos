# Proyecto de Sistemas Distribuidos

Este repositorio contiene el código y las configuraciones necesarias para desplegar y ejecutar un sistema distribuido que realiza operaciones de multiplicación de matrices utilizando múltiples nodos. El sistema está diseñado para funcionar en una red local, utilizando sockets para la comunicación entre los nodos.

## Estructura del Proyecto

- `Cliente/`: Contiene el código del cliente que envía la solicitud de multiplicación de matrices.
- `ServidorPrincipal/`: Contiene el código del servidor principal que coordina las operaciones.
- `ServidorOperacion1/` y `ServidorOperacion2/`: Contienen el código de los servidores de operación que realizan los cálculos parciales.

## Configuración de la Red

Asegúrate de que todos los nodos (cliente, servidor principal, servidores de operación) estén conectados en la misma red local. Los archivos de configuración para cada nodo se encuentran en sus respectivos directorios.

### Direcciones IP y Puertos

- **Servidor Principal**:
  - IP: `192.168.1.2`
  - Puerto: `5000`
  - Comunicación: TCP

- **Servidor de Operación 1**:
  - IP: `192.168.1.3`
  - Puerto: `5001`
  - Comunicación: TCP

- **Servidor de Operación 2**:
  - IP: `192.168.1.4`
  - Puerto: `5002`
  - Comunicación: TCP

- **Cliente**:
  - IP: `192.168.1.5`
  - Puerto: `5003`
  - Comunicación: TCP

## Instrucciones de Compilación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/tuusuario/tu-repo.git
    cd tu-repo
    ```

2. Instala las dependencias necesarias:
    ```bash
    [especificar comando, e.g., pip install -r requirements.txt para Python]
    ```

3. Compila los servidores y el cliente:
    ```bash
    [especificar comandos de compilación, e.g., g++ server.cpp -o server para C++]
    ```

## Ejecución

### Paso 1: Iniciar el Servidor Principal
Ejecuta el servidor principal desde su directorio:

```bash
./ServidorPrincipal/server
```

### Paso 2: Iniciar los Servidores de Operación
Ejecuta los servidores de operación desde sus respectivos directorios:

```bash
./ServidorOperacion1/server
./ServidorOperacion2/server
```

### Paso 3: Iniciar el Cliente
Ejecuta el cliente para enviar una solicitud de cálculo de matrices:

```bash
./Cliente/client
```

## Notas

- Si alguno de los servidores de operación falla, el servidor principal reasignará la tarea al otro servidor disponible.
- Asegúrate de que los puertos especificados estén abiertos en los nodos y que no haya conflictos con otros servicios en ejecución.

## Contribuciones

Si encuentras un error o tienes una mejora que te gustaría sugerir, por favor abre un issue o envía un pull request.
import socket

# Configura el cliente
HOST = '192.168.100.231'  # Cambia por la dirección IP del servidor
PORT = 4000  # Cambia el puerto para que coincida con el del servidor

# Crea un socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while True:
    data = input("Introduce el texto a agregar al archivo (o 'salir' para finalizar): ")

    if data == 'salir':
        break

    # Envía los datos al servidor
    client_socket.send(data.encode('utf-8'))

# Cierra la conexión
client_socket.close()

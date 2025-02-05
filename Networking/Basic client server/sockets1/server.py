import socket

def start_server(host='127.0.0.1', port=12345):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a public host and a port
    server_socket.bind((host, port))
    print(f"Server started on {host}:{port}")

    # Listen for incoming connections (1 connection at a time)
    server_socket.listen(1)
    print("Waiting for a client to connect...")

    # Accept a connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    # Communicate with the client
    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode()
        if data.lower() == 'bye':
            print("Client disconnected.")
            break
        print(f"Client: {data}")

        # Send data to the client
        response = input("Server: ")
        client_socket.send(response.encode())
        if response.lower() == 'bye':
            print("Closing connection.")
            break

    # Close the sockets
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()

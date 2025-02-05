import socket

def start_client(host='127.0.0.1', port=12345):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))
    print(f"Connected to the server at {host}:{port}")

    # Communicate with the server
    while True:
        # Send data to the server
        message = input("Client: ")
        client_socket.send(message.encode())
        if message.lower() == 'bye':
            print("Closing connection.")
            break

        # Receive data from the server
        response = client_socket.recv(1024).decode()
        print(f"Server: {response}")
        if response.lower() == 'bye':
            print("Server disconnected.")
            break

    # Close the socket
    client_socket.close()

if __name__ == "__main__":
    start_client()

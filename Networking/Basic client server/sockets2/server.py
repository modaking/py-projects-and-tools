import asyncio

async def handle_client(reader, writer):
    client_address = writer.get_extra_info('peername')
    print(f"New connection from {client_address}")

    try:
        while True:
            # Receive data from the client
            data = await reader.read(1024)  # Read up to 1024 bytes
            if not data:
                break
            message = data.decode()
            print(f"Client {client_address}: {message}")

            # Echo the message back to the client
            response = f"Server received: {message}"
            writer.write(response.encode())
            await writer.drain()

            if message.lower() == 'bye':
                print(f"Closing connection with {client_address}")
                break
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        print(f"Connection with {client_address} closed.")

async def start_server(host='127.0.0.1', port=12345):
    server = await asyncio.start_server(handle_client, host, port)
    address = server.sockets[0].getsockname()
    print(f"Server started on {address}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(start_server())

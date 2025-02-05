import asyncio

async def start_client(host='127.0.0.1', port=12345):
    reader, writer = await asyncio.open_connection(host, port)
    print(f"Connected to the server at {host}:{port}")

    try:
        while True:
            # Send a message to the server
            message = input("Client: ")
            writer.write(message.encode())
            await writer.drain()

            if message.lower() == 'bye':
                print("Closing connection.")
                break

            # Receive a response from the server
            data = await reader.read(1024)
            print(f"Server: {data.decode()}")
    except Exception as e:
        print(f"Error during communication: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        print("Connection closed.")

if __name__ == "__main__":
    asyncio.run(start_client())

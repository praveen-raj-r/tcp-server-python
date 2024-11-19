import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # Connect to a remote host (it won't actually connect)
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'  # Default to localhost if it fails
    finally:
        s.close()
    return ip

HOST = get_local_ip()
PORT = 12345
BUFFER_SIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server listening on {HOST}:{PORT}...")

while True:
    try:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr} established!")

        # Receive the file name
        file_name = conn.recv(BUFFER_SIZE).decode().strip()
        print(f"Receiving file: {file_name}")

        # Open the file to write the received bytes
        with open(f"received_{file_name}", "wb") as file:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:  # No more data
                    break
                file.write(data)

        print(f"File {file_name} received successfully!")

        # Send a confirmation message back to the client
        conn.sendall(b"File received successfully!")

        # Optionally, keep the connection open for further communication
        # You can add further logic here if you want to continue the communication
        # For example, receive another file or message from the client
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Do not close the connection here; you can keep it open for further communication
        pass

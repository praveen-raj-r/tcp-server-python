import socket

# Function to get the local IP address of the host machine
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket
    s.settimeout(0)  # Set timeout to 0 (non-blocking)
    try:
        # Connect to a remote address (this won't actually establish a connection)
        # Used only to determine the local IP address
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]  # Get the local IP address used in the connection
    except Exception:
        ip = '127.0.0.1'  # Default to localhost if any error occurs
    finally:
        s.close()  # Close the socket
    return ip

# Configuration for the server
HOST = get_local_ip()  # Dynamically determine the local IP address
PORT = 12345  # Port number for the server
BUFFER_SIZE = 1024  # Buffer size for receiving data

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the specified host and port
server_socket.bind((HOST, PORT))
# Start listening for incoming connections (backlog set to 5)
server_socket.listen(5)

print(f"Server listening on {HOST}:{PORT}...")

# Main server loop
while True:
    try:
        # Accept a new client connection
        conn, addr = server_socket.accept()
        print(f"Connection from {addr} established!")

        # Receive the file name from the client
        file_name = conn.recv(BUFFER_SIZE).decode().strip()
        print(f"Receiving file: {file_name}")

        # Open a file to save the received data
        with open(f"received_{file_name}", "wb") as file:
            while True:
                # Receive data from the client
                data = conn.recv(BUFFER_SIZE)
                if not data:  # Break the loop if no more data is received
                    break
                file.write(data)  # Write the received data to the file

        print(f"File {file_name} received successfully!")

        # Send a confirmation message back to the client
        conn.sendall(b"File received successfully!")

        # Keep the connection open if further communication is needed
        # Add additional logic here to handle more client requests if desired

    except Exception as e:
        # Handle any exceptions that occur during the connection or file transfer
        print(f"An error occurred: {e}")
    finally:
        # Do not close the connection immediately, allowing further communication
        # Close connections elsewhere if implementing persistent communication
        pass

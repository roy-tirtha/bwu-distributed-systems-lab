import socket  # Same library as the server - both sides need it

HOST = '127.0.0.1'   # Must match the server's address exactly
PORT = 65432          # Must match the server's port exactly


def start_client():
    student_id = input("Enter Student ID: ")
    name = input("Enter Name: ")
    course = input("Enter Course Name: ")

    # Combine the three fields into one message, separated by commas
    message = f"{student_id},{name},{course}"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))   # Dial the server, like making a phone call

        client_socket.sendall(message.encode())   # Send our message as bytes
        print(f"Sent -> {message}")

        response = client_socket.recv(1024)        # Wait for the server's reply
        print(f"Server says: {response.decode()}")


if __name__ == "__main__":
    start_client()
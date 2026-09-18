import socket  # Python's built-in library for talking over a network

# ---- Configuration ----
HOST = '127.0.0.1'   # Loopback address - means "this same computer", not the internet
PORT = 65432          # Port number - think of it like a specific door on the computer


def validate_data(student_id, name, course):
    """
    Checks whether the received fields look correct.
    Returns (True, "") if everything is fine.
    Returns (False, "reason") if something is wrong.
    """
    if not student_id.isdigit():
        return False, "Student ID must contain only numbers"

    if not name.replace(" ", "").isalpha():
        return False, "Name must contain only letters"

    if not course.strip():
        return False, "Course name cannot be empty"

    return True, ""


def start_server():
    # socket.AF_INET     -> we are using IPv4 addresses (like 127.0.0.1)
    # socket.SOCK_STREAM -> we are using TCP (reliable, ordered delivery, like a phone call)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        server_socket.bind((HOST, PORT))   # Attach this socket to our address + port
        server_socket.listen()             # Start listening for an incoming connection
        print(f"Server is listening on {HOST}:{PORT} ...")

        conn, addr = server_socket.accept()   # Pause here until a client calls in

        with conn:
            print(f"Connected by {addr}")

            data = conn.recv(1024)        # Receive up to 1024 bytes from the client
            decoded = data.decode()       # Convert raw bytes into a normal string

            # We expect the client to send: "id,name,course"
            student_id, name, course = decoded.split(",")

            print(f"Received -> ID: {student_id}, Name: {name}, Course: {course}")

            is_valid, error_msg = validate_data(student_id, name, course)

            if is_valid:
                response = f"CONFIRMED: Student {name} (ID: {student_id}) enrolled in {course}"
            else:
                response = f"REJECTED: {error_msg}"

            conn.sendall(response.encode())   # Send the confirmation back to the client
            print(f"Sent -> {response}")


if __name__ == "__main__":
    start_server()
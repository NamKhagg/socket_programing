import socket
import threading
import json

IP = "127.0.0.1"
PORT = 3030

users = {
    "User 1": "password123",
    "User 2": "abc123"
}

def handle_client(client_socket, client_address):
    print(f"Client socket {client_socket}")
    print(f"Received connection from {client_address}")

    try:
        login_data = client_socket.recv(1024)

        if not login_data:
            return

        login_request = json.loads(login_data.decode())

        request_type = login_request.get("type")
        request_username = login_request.get("username")
        request_password = login_request.get("password")

        if request_type == "LOGIN":
            if request_username in users and users.get(request_username) == request_password:
                client_socket.sendall("Login successful".encode())
            else:
                client_socket.sendall("Login failed".encode())
                return
        else: 
            client_socket.sendall("Invalid request type".encode())
            return
    
        print(type(login_request))
        print(f"Received login request: {login_request}")
        
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            
            message = data.decode()

            print(f"Received message: {message}")

            client_socket.sendall(f"I have received your message : {message}".encode())
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        client_socket.close()
        print(f"Connection with {client_address} closed")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((IP, PORT))
print(f"Server is listening on {IP}:{PORT}")


server_socket.listen()

try:
    while True:

        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        
        client_thread.start()
except KeyboardInterrupt:
    print("Server is shutting down.")
finally:
    server_socket.close();


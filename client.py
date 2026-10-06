import socket
import json

IP = "127.0.0.1"
PORT = 3030

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

print(client_socket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF))

print(f"Connected to server at {IP}:{PORT}")

request = {
    "type": "LOGIN",
    "username": "User 1",
    "password": "password123"
}

json_data = json.dumps(request)
client_socket.sendall(json_data.encode())

login_response = client_socket.recv(1024).decode()

if login_response == "Login successful":
    print("Login successful. You can now send messages to the server.")
else: 
    print(login_response)
    print("Login failed. Closing connection.")
    client_socket.close()
    exit()

while True:

    message = input(f"Enter message did you want to send to the server (Enter 'exit' to quit): ").strip()
    
    if not message or message.lower() == "exit":
        break
    
    client_socket.sendall(message.encode())

    server_response = client_socket.recv(1024).decode()

    if not server_response:
        print("Server closed the connection.")
        break
        
    print(f"Received response from server: {server_response}")

client_socket.close()
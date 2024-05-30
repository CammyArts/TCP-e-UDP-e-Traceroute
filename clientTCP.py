import socket

def tcp_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5000))
    client.send("Hello from TCP client!".encode())
    response = client.recv(4096)
    print(response.decode())

if __name__ == "__main__":
    tcp_client()

# nome: Camila Rodrigues
import socket
import threading
import random

# Função para lidar com clientes TCP
def handle_tcp_client(client_socket):
    try:
        while True:
            request = client_socket.recv(1024)
            if not request:
                break
            print(f"[TCP] Recebido: {request.decode()}")
            client_socket.send("ACK de TCP Servidor".encode())
    except ConnectionResetError:
        print("Conexão TCP fechada pelo cliente.")
    finally:
        client_socket.close()

# Função para lidar com clientes UDP
def handle_udp_client(data, addr, server_socket):
    print(f"[UDP] Recebido: {data.decode()} de {addr}")
    server_socket.sendto("ACK de UDP Servidor".encode(), addr)

# Servidor TCP
def tcp_server():
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind(("0.0.0.0", 5000))
    tcp_server_socket.listen(5)
    print("[TCP] Servidor está escutando...")

    while True:
        client_socket, addr = tcp_server_socket.accept()
        print(f"[TCP] Conexão aceita de: {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_tcp_client, args=(client_socket,))
        client_handler.start()

# Servidor UDP
def udp_server():
    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server_socket.bind(("0.0.0.0", 5001))
    print("[UDP] Servidor está escutando...")

    while True:
        data, addr = udp_server_socket.recvfrom(1024)
        handle_udp_client(data, addr, udp_server_socket)

def main():
    tcp_server_thread = threading.Thread(target=tcp_server)
    udp_server_thread = threading.Thread(target=udp_server)

    tcp_server_thread.start()
    udp_server_thread.start()

    tcp_server_thread.join()
    udp_server_thread.join()

if __name__ == "__main__":
    main()

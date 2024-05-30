# nome: Camila Rodrigues
import socket
import threading
import random

def get_response(message):
    responses = [
        "Interessante, me conte mais.",
        "Hmm, entendo.",
        "Isso é intrigante!",
        "Parece emocionante!",
        "Que legal!",
        "Que interessante!",
        "Que legal! Continue...",
        "Muito interessante, diga-me mais.",
        "Estou ouvindo, pode continuar.",
        "Fascinante, continue...",
        "Entendi, o que mais você gostaria de compartilhar?",
    ]
    return random.choice(responses)

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

# Função para lidar com clientes do chat
def handle_chat_client(client_socket, clients):
    try:
        while True:
            msg = client_socket.recv(1024)
            if not msg:
                break
            print(f"[Chat] Mensagem recebida: {msg.decode()}")
            broadcast_message(msg, clients, client_socket)
    except ConnectionResetError:
        print("Conexão de chat fechada pelo cliente.")
    finally:
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()

# Função para transmitir uma mensagem para todos os clientes do chat
def broadcast_message(message, clients, sender_socket):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.send(message)
            except Exception as e:
                print(f"Erro ao enviar mensagem para um cliente: {e}")
                client_socket.close()
                clients.remove(client_socket)

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

# Servidor de chat
def chat_server():
    chat_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chat_server_socket.bind(("0.0.0.0", 5002))
    chat_server_socket.listen(5)
    print("[Chat] Servidor de chat está escutando...")

    clients = []

    while True:
        client_socket, addr = chat_server_socket.accept()
        print(f"[Chat] Conexão aceita de: {addr[0]}:{addr[1]}")
        clients.append(client_socket)
        client_handler = threading.Thread(target=handle_chat_client, args=(client_socket, clients))
        client_handler.start()

def main():
    tcp_server_thread = threading.Thread(target=tcp_server)
    udp_server_thread = threading.Thread(target=udp_server)
    chat_server_thread = threading.Thread(target=chat_server)

    tcp_server_thread.start()
    udp_server_thread.start()
    chat_server_thread.start()

    tcp_server_thread.join()
    udp_server_thread.join()
    chat_server_thread.join()

if __name__ == "__main__":
    main()


# ping é um comando pra ver se o hut ta ativo inclementado no python
# traceroute inclementado no python
# nome: Camila Rodrigues
import socket
import os
import subprocess
import platform
import shutil

def udp_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto("Hello from UDP client!".encode(), ('127.0.0.1', 5001))
    data, addr = client.recvfrom(4096)
    print(data.decode())

def tcp_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5000))
    client.send("Hello from TCP client!".encode())
    response = client.recv(4096)
    print(response.decode())

def chat_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5002))
    while True:
        msg = input("Digite sua mensagem (ou 'sair' para terminar): ")
        if msg.lower() == 'sair':
            break
        client.send(msg.encode())
        response = client.recv(4096)
        print(f"Servidor: {response.decode()}")
    client.close()

def perform_traceroute(host):
    try:
        # Determine the command based on the operating system
        if platform.system() == "Windows":
            command = "tracert"
        else:
            command = "traceroute"

        # Check if the command is available
        if shutil.which(command) is None:
            print(f"Erro: O comando '{command}' não está disponível no sistema.")
            return

        print(f"Executando {command} para {host}...")
        result = subprocess.run([command, host], capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar {command}: {e}")

def ping(host):
    try:
        result = subprocess.run(["ping", "-c", "4", host], capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar ping: {e}")

def main():
    while True:
        print("\nMenu:")
        print("1. Testar TCP")
        print("2. Testar UDP")
        print("3. Traceroute")
        print("4. Ping")
        print("5. Chat")
        print("6. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            tcp_client()
        elif choice == '2':
            udp_client()
        elif choice == '3':
            host = input("Digite o endereço do host: ")
            perform_traceroute(host)
        elif choice == '4':
            host = input("Digite o endereço do host: ")
            ping(host)
        elif choice == '5':
            chat_client()
        elif choice == '6':
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()

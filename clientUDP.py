import socket

def udp_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto("Hello from UDP client!".encode(), ('127.0.0.1', 5001))
    data, addr = client.recvfrom(4096)
    print(data.decode())

if __name__ == "__main__":
    udp_client()

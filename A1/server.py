from socket import *
import sys


def get_open_port():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port

req_code = sys.argv[1]

n_port = get_open_port();
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', n_port))
serverSocket.listen(1)
fo = open("server.txt", "w+")
fo.write('SERVER_PORT: '+ str(n_port))
fo.close()

print("SERVER_PORT: " + str(n_port))

messages = []

while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = int(connectionSocket.recv(1024).decode())

    if int(req_code) != sentence:
        r_port = 0
        connectionSocket.send(str(r_port).encode())
        # connectionSocket.close()
    else:
        r_port = get_open_port()
        connectionSocket.send(str(r_port).encode())
        # connectionSocket.close()

        serverSocketUDP = socket(AF_INET, SOCK_DGRAM)
        serverSocketUDP.bind(('', r_port))

        while True:
            message, clientAddress = serverSocketUDP.recvfrom(1024)

            message = message.decode()
            # print(message)

            if (message == "GET"):
                for i in range(len(messages)):
                    serverSocketUDP.sendto(messages[i].encode(), clientAddress)
                serverSocketUDP.sendto("NO MSG".encode(), clientAddress)


            elif (message == "TERMINATE"):
                serverSocketUDP.close()
                # serverSocket.close()
                connectionSocket.close()
                exit(0)
            else:
                clientMsg = str(r_port) + ": " + message
                messages.append(clientMsg)
                break
        serverSocketUDP.close()
    connectionSocket.close()
























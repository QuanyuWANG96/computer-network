from socket import *
import sys
import socket

server_address = sys.argv[1]
n_port = int(sys.argv[2])
req_code = int(sys.argv[3])
message = sys.argv[4]

# client try to connect server via TCP
clientSocketTCP = socket.socket(AF_INET, SOCK_STREAM)
clientfile = open("client.txt", "a")
try:
    clientSocketTCP.connect((server_address, n_port))
except ConnectionRefusedError as err:
    clientfile.write("Error server_unavailable\n\n")
    clientfile.close()
    sys.stderr.write("Error server_unavailable\n")
    sys.exit(1)

# send req_code and check if it is match
clientSocketTCP.send(str(req_code).encode())
modifiedSentence = clientSocketTCP.recv(1024)

r_port = int(modifiedSentence.decode())

if r_port == 0:
    clientSocketTCP.close()
    clientfile.write("Invalid req_code\n\n")
    clientfile.close()
    sys.stderr.write("Invalid rep_code\n")
    sys.exit(0)

clientfile.write("r_port: " + str(r_port) + "\n" )
clientSocketTCP.close()

# send GET to server and show all the exist message
clientSocketUDP = socket.socket(AF_INET, SOCK_DGRAM)
getCommand = "GET"
clientSocketUDP.sendto(getCommand.encode(), (server_address, r_port))

while True:
    messageFromS, serverAddr = clientSocketUDP.recvfrom(2048)
    messageFromS = messageFromS.decode()
    print(messageFromS)
    if messageFromS == "NO MSG":
        clientfile.write(messageFromS + "\n\n")
        break
    clientfile.write(messageFromS)
    clientfile.write("\n")

clientfile.close()
clientSocketUDP.sendto(message.encode(), (server_address, r_port))

if message == "TERMINATE":
    clientSocketUDP.close()
    exit(0)

keyboardInput = sys.stdin.readline()
clientSocketUDP.close()
if keyboardInput != None:
    exit(0)

















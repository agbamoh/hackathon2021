import socket
from socket import *
import time
import getch
import keyboard


serverPort_tcp = 0


# Colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# UDP Server client side.
# Simple UDP Client function, that listens to the server and prints the messages from the server side.
def UDPClinet():
    global serverPort_tcp
    serverName = ''
    serverPort = 13117
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.setsockopt(SOL_SOCKET,SO_REUSEPORT , 1)
    clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    clientSocket.bind((serverName, serverPort))
    print("Client started, listening for offer requests...")
   
        
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    if ((modifiedMessage[0] == 254) & (modifiedMessage[1] == 237) & (modifiedMessage[2] == 190) & (
            modifiedMessage[3] == 239)):
        port = [modifiedMessage[5], modifiedMessage[6]]
        serverPort_tcp = int.from_bytes(port, 'little')
        print(bcolors.OKGREEN + "Received offer from " + serverAddress[0] + ",attempting to connect...")
        clientSocket.close()
        return serverAddress[0], serverPort_tcp
    else:
        return UDPClinet()


# TCP Server client side
# This is where the game happen, the client press on the key and we print and claculate how many.
# inputs the user inserted, we do that in the while loop, it takes 10 seconeds for the player to enter the code.
# *since the msvcrt.getch() is blocking function we used "if msvcrt.kbhit()".
def TCPClinet(server_ip, server_port):
    global serverPort_tcp
    serverName = server_ip
    serverPorttcp = server_port
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPorttcp))
    team_name = "FCB"
    try:
        clientSocket.send(team_name.encode())
    except:
        pass
    modifiedSentence = clientSocket.recv(1024)
    print(modifiedSentence.decode())
    end = time.time() + 10
    flag = True
    while flag:
        

       # char = getch.getch():
        
        
        try:
            keyboard.on_press_key(x, lambda _:clientSocket.send(x))
            flag = False
            #clientSocket.send(char)
        except:
            flag = False
        break

    msg = clientSocket.recv(1024)

    print(msg.decode())
    print("Server disconnected, listening for offer requests...")


# main function with a while loop that runs the client sides.
if __name__ == '__main__':
    while True:
        server_ip, server_port = UDPClinet()
        TCPClinet(server_ip, server_port)

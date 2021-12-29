from socket import *
import time
import threading
import MathsGame
import scapy.all as Scapy

Client_sockets = []


def get_ip_address(interface):
    return Scapy.get_if_addr(interface)


# UDP Server Side
# This function starts the udp server, the udp server and disconnect after 10 seconeds.
def UDPServer(interface=Scapy.conf.iface):
    serverport = 13117
    serverSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    serverSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    TCPPort = TCPServer(interface)
    print(TCPPort)
    message_bytes = []
    
    message_bytes.extend(bytes.fromhex("abcddcba"))
    message_bytes.extend([2])
    message_bytes.extend(TCPPort.to_bytes(2, 'little'))
    print("Server started, listening on IP address " + get_ip_address(interface))
    for i in range(10):
        try:
            serverSocket.sendto(bytes(message_bytes), ('<broadcast>', serverport))
            time.sleep(1)
        except:
            break

    MathsGame.prepare_players()
    print(len(Client_sockets))
    for (x, y) in Client_sockets:
        gamethread = threading.Thread(target=MathsGame.game, args=(x, y)).start()
    time.sleep(10)
    msg = MathsGame.print_wins()
    print(msg)
    for (a, b) in Client_sockets:
        a.send(msg.encode())
    #time.sleep(2)
    serverSocket.close()
    for (a, b) in Client_sockets:
        a.close()
    Client_sockets.clear()
    print("Game over, sending out offer requests...")


# TCP Server Side.
# This function starts the TCP server and run the game and calls the game
# function in the Game module to calculate the result and disconnect after 10 seconds.
def TCPServer(interface):
    serverPort = 0
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.settimeout(10)
    serverSocket.bind((get_ip_address(interface), serverPort))
    TCPPort = serverSocket.getsockname()[1]
    serverSocket.listen(1)
    client_arr = []

    def _accpet_thread():
        flag = True
        while flag:
            try:
                connectionSocket, addr = serverSocket.accept()
                Client_sockets.append((connectionSocket, addr))
                Clinethread = threading.Thread(target=MathsGame.team_name, args=(connectionSocket, addr)).start()
                client_arr.append(Clinethread)
            except:
                flag = False

    TCPThread = threading.Thread(target=_accpet_thread)
    TCPThread.start()
    return TCPPort


if __name__ == '__main__':
    while 1:
        UDPServer(Scapy.conf.iface)
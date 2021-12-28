import random

operators = ['+', '-', '*', '/', '%']
maths_calc = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b,
    '%': lambda a, b: a % b

}


def generate_math_equation():
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    idx = random.randint(0, 4)
    opr = operators[idx]
    while not maths_calc[opr](a, b) in range(10):
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        idx = random.randint(0, 4)
        opr = operators[idx]
    equation_str = str(a) + opr + str(b) + '?'
    return a, b, opr, equation_str


x, y, op, eq = generate_math_equation()

arr = []
player1 = ()
player2 = ()
winner = 0


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


# recieve and saves the team names in a tuple.
def team_name(connectionSocket, addr):
    try:
        player_name = connectionSocket.recv(1024)
        arr.append((player_name.decode(), connectionSocket, addr))
    except:
        pass


# starts the game, sends messages to the clients of their names, and notes them to start the game.
def game(connectionSocket, addr):
    global x
    global y
    global op
    global eq
    global player2
    global player1
    global winner
    msg = "Welcome to Quick Maths.\n"
    pl1 = player1[0]
    msg = msg + bcolors.OKBLUE + "Player 1:" + pl1 + "\n"

    pl2 = player2[0]
    msg = msg + bcolors.FAIL + "Player 2:" + pl2 + "\n"
    msg = msg + bcolors.WARNING + "Please answer the following question as fast as you can:\n"

    answer = maths_calc[op](x, y)
    msg = msg + "How much is " + eq + "\n"
    try:
        connectionSocket.send(msg.encode())
    except:
        pass
    h = True
    while h:
        try:
            x = connectionSocket.recv(1024).decode()
        except:
            h = False
            connectionSocket.close()
            arr.clear()
            player1 = ()
            player2 = ()

            break
        if x == str(answer):
            if (connectionSocket, addr) == (pl1[1], pl1[2]):
                winner = 1
            else:
                winner = 2
            h = False


# Prints the winner(with colors ofcourse :) ).
def print_wins():
    global x
    global y
    global op
    global eq
    ans = maths_calc[op](int(x), int(y))

    msg = "Game over!\nThe correct answer was " + str(ans) + "!\n"

    if winner == 1:
        player = player1[0]
    else:
        player = player2[0]
    msg += "Congratulations to the winner: " + player
    return msg


# Splits the teams in a random manner.
def prepare_players():
    global player1
    global player2
    while True:
        if len(arr) >1:
            break

    player1 = arr[0]
    player2 = arr[1]

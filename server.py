import socket
import threading

# установка размеров окна
screen_width = 800
screen_height = 600

# список всех игроков на поле
players = {}

# создание сервера
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5000))
server.listen()

# функция для обработки сообщений от клиента
def handle_client(conn, addr):
    global players
    print(f"New connection from {addr}")
    conn.send(f"Welcome to the game! Enter your name:".encode())
    player_name = conn.recv(1024).decode('cp1251')
    color_choice = conn.recv(1024).decode()
    if color_choice == "r":
        player_color = (255, 0, 0)
    elif color_choice == "g":
        player_color = (0, 255, 0)
    elif color_choice == "b":
        player_color = (0, 0, 255)
    else:
        player_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    players[player_name] = {"x": screen_width // 2, "y": screen_height // 2, "color": player_color}
    conn.send(f"Your color is {color_choice}".encode())
    while True:
        try:
            data = conn.recv(1024).decode()
            if data == "get":
                # отправка координат всех игроков на поле
                data = ""
                for name in players:
                    data += f"{name}:{players[name]['x']},{players[name]['y']},{players[name]['color'][0]},{players[name]['color'][1]},{players[name]['color'][2]};"
                conn.send(data.encode())
            else:
                # обновление координат текущего игрока
                x, y = data.split(",")
                players[player_name]["x"] = int(x)
                players[player_name]["y"] = int(y)
        except:
            del players[player_name]
            print(f"Connection from {addr} closed")
            conn.close()
            break

# функция для запуска сервера и обработки соединений
def start_server():
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

start_server()
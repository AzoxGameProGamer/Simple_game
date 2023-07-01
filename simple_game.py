import pygame
from pygame.locals import *
import random

pygame.init()

# установка размеров окна
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# установка цвета фона
background_color = (255, 255, 255)

# окно выбора имени игрока и цвета
player_name = input("Введите имя игрока: ")
color_choice = input("Выберите цвет (r - красный, g - зеленый, b - синий): ")
if color_choice == "r":
    player_color = (255, 0, 0)
elif color_choice == "g":
    player_color = (0, 255, 0)
elif color_choice == "b":
    player_color = (0, 0, 255)
else:
    player_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# установка начальной позиции игрока
player_x = screen_width // 2
player_y = screen_height // 2

# установка скорости перемещения игрока
player_speed = 0.5

# создание объекта текста для отображения имени игрока
font = pygame.font.Font(None, 36)
player_name_text = font.render(player_name, True, (0, 0, 0))
player_name_rect = player_name_text.get_rect()
player_name_rect.centerx = player_x
player_name_rect.bottom = player_y - 25

# установка задержки между выстрелами
fire_delay = 500
last_fire_time = pygame.time.get_ticks()

# список всех игроков на поле
players = []

# игровой цикл
running = True
while running:
    # обработка событий
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            # проверка задержки между выстрелами
            current_time = pygame.time.get_ticks()
            if current_time - last_fire_time >= fire_delay:
                # создание нового объекта выстрела
                bullet_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                bullet_x, bullet_y = player_x, player_y
                bullet_speed = 10
                bullet_direction = pygame.math.Vector2(pygame.mouse.get_pos()) - pygame.math.Vector2(player_x, player_y)
                bullet_direction.normalize_ip()
                players.append({"x": bullet_x, "y": bullet_y, "color": bullet_color, "speed": bullet_speed, "direction": bullet_direction})
                last_fire_time = current_time

    # получение состояния клавиш
    keys = pygame.key.get_pressed()

    # перемещение игрока в зависимости от нажатых клавиш
    if keys[K_w]:
        player_y -= player_speed
    if keys[K_s]:
        player_y += player_speed
    if keys[K_a]:
        player_x -= player_speed
    if keys[K_d]:
        player_x += player_speed

    # ограничение перемещения игрока в пределах окна
    if player_x < 0:
        player_x = 0
    elif player_x > screen_width:
        player_x = screen_width
    if player_y < 0:
        player_y = 0
    elif player_y > screen_height:
        player_y = screen_height

    # обновление положения объекта текста с именем игрока
    player_name_rect.centerx = player_x
    player_name_rect.bottom = player_y - 25

    # обновление положения всех игроков на поле (включая выстрелы)
    for player in players:
        player["x"] += player["direction"].x * player["speed"]
        player["y"] += player["direction"].y * player["speed"]

    # удаление выстрелов, которые вышли за пределы окна
    players = [player for player in players if 0 <= player["x"] <= screen_width and 0 <= player["y"] <= screen_height]

    # отрисовка игровых объектов
    screen.fill(background_color)
    pygame.draw.circle(screen, player_color, (player_x, player_y), 20)
    screen.blit(player_name_text, player_name_rect)
    for player in players:
        pygame.draw.circle(screen, player["color"], (int(player["x"]), int(player["y"])), 5)
    pygame.display.update()

# завершение работы pygame
pygame.quit()
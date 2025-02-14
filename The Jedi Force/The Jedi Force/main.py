import pygame
import sys
import json
import time
import random

# Установка размеров экрана
WIDTH = 1920
HEIGHT = 1080

# Определение цветов
VIOLET = (0, 0, 34)
ORANGE = (226, 132, 19)
WHITE = (251, 245, 243)
DIM_ORANGE = (151, 97, 33)
DIM_WHITE = (210, 210, 210)
GREEN = (56, 151, 27)
RED = (183, 27, 27)

# Глобальные переменные для управления состоянием игры
transition = 0 # Текущий экран (0 - стартовый, 1 - выбор предмета, 2 - настройки, 3 - вопросы, 4 - результаты)
questions_transition = 0# Текущий вопрос в викторине
score = 0 # Счет игрока
delay = 0 # Задержка для перехода между вопросами
volume = 1 # Громкость звука (1 - включен, 0 - выключен)

# Инициализация Pygame и звуковой системы
pygame.init()
pygame.mixer.init()

# Создание окна с изменяемым размером
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Викторина")

# Загрузка иконки для окна
img = pygame.image.load('The Jedi Force/data/icon.png')
pygame.display.set_icon(img)

# Загрузка звуковых файлов
right = pygame.mixer.Sound("The Jedi Force/data/правильно.mp3")
wrong = pygame.mixer.Sound("The Jedi Force/data/неправильно.mp3")
playsound = pygame.mixer.Sound("The Jedi Force/data/ход_игры.mp3")
click = pygame.mixer.Sound("The Jedi Force/data/клик.mp3")

# Загрузка вопросов из JSON-файла
with open("The Jedi Force/data/questions.json", "r", encoding='utf-8') as file:
    data = json.load(file)

# Функция для отрисовки текста на экране
def write_text(type1, content, size, color, x, y, transfer_type=0, options=0):
    font = pygame.font.Font(f'The Jedi Force/data/{type1}', size)
    if transfer_type != 0:
        words = content.split(' ')
        result = []
        current_line = []

        for i, word in enumerate(words):
            current_line.append(word)
            if (i + 1) % transfer_type == 0 or i == len(words) - 1:
                result.append(' '.join(current_line))
                current_line = []
        a = 0
        for i in result:
            text = font.render(i, False, color)
            text_rect = text.get_rect()
            if options == 1:
                text_rect.centerx = x + 220
            if options == 2:
                text_rect.centerx = WIDTH // 2
            if options == 3:
                text_rect.centerx = x + 105
            screen.blit(text, (text_rect.x, y + a * 60))
            a += 1

    else:
        text = font.render(content, False, color)
        screen.blit(text, (x, y))

# Функция для создания кнопок
def create_button(color1, color2, setting, radius, type1, content, size, color_text1, color_text2, x, y,
                  transfer_type=0, options=0, specific=0, answer=''):
    global transition, subject1, questions_transition, score, delay, volume
    object1 = pygame.Rect(setting)

    mouse_position = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    if object1.collidepoint(mouse_position):
        if mouse_pressed[0]:
            if volume == 1 and specific == 0:
                click.play()
            time.sleep(0.1)

            # Обработка действий в зависимости от текста кнопки
            if content == 'ВЫХОД':
                sys.exit()
            elif content == 'ВЫБРАТЬ ПРЕДМЕТ':
                transition = 1
            elif content == 'НАСТРОЙКИ':
                transition = 2
            elif content == 'НАЗАД':
                transition = 0
            elif content == 'В МЕНЮ':
                questions_transition = 0
                transition = 1
            elif content == 'ВКЛЮЧИТЬ ЗВУК':
                volume = 1
            elif content == 'ВЫКЛЮЧИТЬ ЗВУК':
                volume = 0
            elif specific == 1:
                if content == answer:
                    score += 1
                    pygame.draw.rect(screen, GREEN, pygame.Rect(setting), border_radius=radius)
                    write_text(type1, content, size, color_text1, x, y, transfer_type, options)
                    if volume == 1:
                        right.play()
                else:
                    pygame.draw.rect(screen, RED, pygame.Rect(setting), border_radius=radius)
                    write_text(type1, content, size, color_text1, x, y, transfer_type, options)
                    if volume == 1:
                        wrong.play()
                delay = 1

            else:
                transition = 3
                score = 0
                questions_list(content)
        else:
            pygame.draw.rect(screen, color2, pygame.Rect(setting), border_radius=radius)
            write_text(type1, content, size, color_text2, x, y, transfer_type, options)
    else:
        pygame.draw.rect(screen, color1, pygame.Rect(setting), border_radius=radius)
        write_text(type1, content, size, color_text1, x, y, transfer_type, options)

# Функция для выбора случайных вопросов из списка
def questions_list(subject):
    global subject1, data2, data
    data1 = list(data[subject]) # Получение списка вопросов для выбранного предмета
    data2 = []
    subject1 = subject
    for i in range(0, 10, 1):
        random1 = random.randint(0, len(data1) - 1)
        data2.append(data1[random1])
        data1.pop(random1)

# Функция для отображения текущего вопроса
def questions():
    global delay
    delay = 0
    write_text('seravek.otf', data2[questions_transition]['question'], 64, ORANGE, 500, 50, 4, 2)
    write_text('seravek.otf', f'{questions_transition + 1}/10', 64, WHITE, 1750, 200)
    create_button(ORANGE, DIM_ORANGE, [255, 300, 470, 220], 30, 'seravek.otf',
                  data2[questions_transition]['options'][0], 25, WHITE, DIM_WHITE, 270, 300, 3, 1, 1,
                  answer=data2[questions_transition]['answer'])
    create_button(ORANGE, DIM_ORANGE, [1180, 300, 470, 220], 30, 'seravek.otf',
                  data2[questions_transition]['options'][1], 25, WHITE, DIM_WHITE, 1195, 300, 3, 1, 1,
                  answer=data2[questions_transition]['answer'])
    create_button(ORANGE, DIM_ORANGE, [255, 600, 470, 220], 30, 'seravek.otf',
                  data2[questions_transition]['options'][2], 25, WHITE, DIM_WHITE, 270, 600, 3, 1, 1,
                  answer=data2[questions_transition]['answer'])
    create_button(ORANGE, DIM_ORANGE, [1180, 600, 470, 220], 30, 'seravek.otf',
                  data2[questions_transition]['options'][3], 25, WHITE, DIM_WHITE, 1195, 600, 3, 1, 1,
                  answer=data2[questions_transition]['answer'])
    create_button(ORANGE, DIM_ORANGE, [720, 900, 524, 85], 30, 'seravek.otf', 'В МЕНЮ', 40, WHITE, DIM_WHITE, 910, 920)

# Функция для отображения стартового экрана
def start_screen():
    write_text('activistka.ttf', 'ЕГЭ ВИКТОРИНА', 128, ORANGE, 450, 90)
    create_button(ORANGE, DIM_ORANGE, [697, 370, 524, 85], 30, 'seravek.otf', 'ВЫБРАТЬ ПРЕДМЕТ', 40, WHITE, DIM_WHITE,
                  770, 390)
    create_button(ORANGE, DIM_ORANGE, [697, 550, 524, 85], 30, 'seravek.otf', 'НАСТРОЙКИ', 40, WHITE, DIM_WHITE, 850,
                  570)
    create_button(ORANGE, DIM_ORANGE, [697, 730, 524, 85], 30, 'seravek.otf', 'ВЫХОД', 40, WHITE, DIM_WHITE, 880, 750)

# Функция для отображения экрана выбора предмета
def choose_subject_screen():
    global volume1
    write_text('activistka.ttf', 'ВЫБРАТЬ ПРЕДМЕТ', 96, WHITE, 500, 90)
    create_button(ORANGE, DIM_ORANGE, [720, 900, 524, 85], 30, 'seravek.otf', 'НАЗАД', 40, WHITE, DIM_WHITE, 910, 920)

    # Создание кнопок для выбора предмета
    for i in range(0, len(data), 1):
        if 1 <= i + 1 <= 5:
            y = 250
        elif 6 <= i + 1 <= 10:
            y = 450
        elif 11 <= i + 1 <= 14:
            y = 650
        if i + 1 == 1 or i + 1 == 6 or i + 1 == 11:
            x = 60
        elif i + 1 == 2 or i + 1 == 7 or i + 1 == 12:
            x = 440
        elif i + 1 == 3 or i + 1 == 8 or i + 1 == 13:
            x = 830
        elif i + 1 == 4 or i + 1 == 9 or i + 1 == 14:
            x = 1230
        elif i + 1 == 5 or i + 1 == 10:
            x = 1620
        create_button(ORANGE, DIM_ORANGE, [x, y, 233, 128], 30, 'seravek.otf', list(data.keys())[i], 27, WHITE,
                      DIM_WHITE, x + 12, y + 40, options=3, transfer_type=1)

# Функция для отображения экрана настроек
def settings_screen():
    write_text('activistka.ttf', 'НАСТРОЙКИ', 96, WHITE, 700, 90, transfer_type=2, options=2)
    create_button(ORANGE, DIM_ORANGE, [700, 900, 524, 85], 30, 'seravek.otf', 'НАЗАД', 40, WHITE, DIM_WHITE, 910, 920,
                  transfer_type=2, options=2)

    # Кнопка для включения/выключения звука
    if volume == 0:
        text = 'ВКЛЮЧИТЬ ЗВУК'
    else:
        text = 'ВЫКЛЮЧИТЬ ЗВУК'
    create_button(ORANGE, DIM_ORANGE, [700, 500, 524, 85], 30, 'seravek.otf', text, 40, WHITE, DIM_WHITE, 910, 515,
                  transfer_type=2, options=2)

# Функция для отображения результатов теста
def results(score1):
    write_text('activistka.ttf', 'РЕЗУЛЬТАТЫ ТЕСТА', 96, WHITE, 500, 90)
    create_button(ORANGE, DIM_ORANGE, [710, 900, 524, 85], 30, 'seravek.otf', 'В МЕНЮ', 40, WHITE, DIM_WHITE, 910, 920)
    text = f'Ваш результат за тест по предмету {subject1.lower()}: {score1}/10. Спасибо за прохождение теста именно в ' \
           f'нашем приложении! '

    pygame.draw.rect(screen, ORANGE, [121, 356, 1680, 230], border_radius=30)
    write_text('seravek.otf', text, 64, WHITE, 121, 356, transfer_type=6, options=2)

# Управление звуком
volume1 = 1
while True:
    if volume1 == 1 and volume == 1:
        playsound.play(-1) # Воспроизведение фоновой музыки
        volume1 = 0
    elif volume1 == 0 and volume == 0:
        playsound.stop() # Остановка фоновой музыки
        volume1 = 1

    
    screen.fill(VIOLET) # Заливка экрана цветом
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Отображение текущего экрана в зависимости от значения переменной transition            
    if transition == 0:
        start_screen()
    elif transition == 1:
        choose_subject_screen()
    elif transition == 2:
        settings_screen()
    elif transition == 3:
        questions()
    elif transition == 4:
        results(score)

    pygame.display.flip() # Обновление экрана

     # Обработка задержки перед переходом к следующему вопросу
    if delay == 1:
        time.sleep(0.5)
        if questions_transition != 9:
            questions_transition += 1
        else:
            transition = 4
            delay = 0

import os #для работы с файловой системой
import pygame #библиотека для работы с графикой и игровым окном
import gc #созданная библиотека
import random #импортируем библиотеку random, которая позволяет работать с генерацией случайных чисел.
from pygame import display, event, image, transform #импортируем элементы из библиотеки (display-управления окном, event-обработка событий, image-работа с изображениями)
from time import sleep #функция sleep для создания пауз 

IMAGE_SIZE = 128 #размер изображения в пикселях
SCREEN_SIZE = 512 #размер экрана в пикселях
NUM_TILES_SIDE = 4 #количество плиток по стороне в игре
NUM_TILES_TOTAL = 16 #общее количество плиток в игре
MARGIN = 8 #отступ между плитками в игре

ASSET_DIR = 'assets' #папка, где хранятся ресурсы для игры
#Здесь создается список `ASSET_FILES`, содержащий имена файлов из папки `ASSET_DIR`, но только те файлы, у которых расширение `.png`. Он использует list comprehension для фильтрации файлов по расширению
ASSET_FILES = [x for x in os.listdir(ASSET_DIR) if x[-3:].lower() == 'png']
#проверяет, что количество файлов в списке `ASSET_FILES` равно 8. Если условие не выполняется, возникнет ошибка.
assert len(ASSET_FILES) == 8
#создаем словарь animals_count, где ключами являются имена животных из ASSET_FILES, а значениями - количество встречающихся животных (начально установлено в 0)
animals_count = dict((a, 0) for a in ASSET_FILES)
#определяем функцию available_animals(), которая возвращает список животных, у которых количество встречающихся их картинок меньше двух
def available_animals():
    return [animal for animal, count in animals_count.items() if count < 2]

class Animal: #создаем класс Animal, описывающий животное в игре
    def __init__(self, index): #определяем метод init, который инициализирует объект Animal с заданным индексом
        self.index = index #устанавливаем индекс для конкретного животного
        self.name = random.choice(available_animals()) #выбираем случайное доступное животное для данного экземпляра Animal
        self.image_path = os.path.join(ASSET_DIR, self.name) #создаем путь к изображению животного, объединяя директорию из gc.ASSET_DIR и имя файла животного
        self.row = index // NUM_TILES_SIDE #вычисляем строку и столбец, на котором будет находиться данное животное на игровом поле
        self.col = index % NUM_TILES_SIDE #инициализируем флаг skip как False, чтобы указать, что данное животное не было пропущено
        self.skip = False
        self.image = image.load(self.image_path) #загружаем изображение животного по указанному пути
        self.image = transform.scale(self.image, (IMAGE_SIZE - 2 * MARGIN, IMAGE_SIZE - 2 * MARGIN)) #изменяем размер изображения, обрезая его на gc.MARGIN пикселей со всех сторон
        self.box = self.image.copy() #создаем копию изображения животного для отображения "закрытой" плитки
        self.box.fill((200, 200, 200)) #заполняем изображение "закрытой" плитки серым цветом
        animals_count[self.name] += 1 #увеличиваем количество встречающихся картинок данного животного на единицу, чтобы контролировать доступность животных при создании новых объектов Animal
#объявляем функцию find_index_from_xy с аргументами x и y, которая будет находить индекс элемента по координатам x и y на экране
def find_index_from_xy(x, y):
    row = y // IMAGE_SIZE #вычисляем строку (row) по вертикали, делением координаты y на размер изображения (определенный в gc.IMAGE_SIZE)
    col = x // IMAGE_SIZE #вычисляем столбец (col) по горизонтали, делением координаты x на размер изображения
    index = row * NUM_TILES_SIDE + col  #вычисляем индекс элемента в одномерном списке, учитывая его расположение в двумерном массиве, используя количество столбцов (определенное в gc.NUM_TILES_SIDE)
    return row, col, index

pygame.init() #инициализируем библиотеку Pygame
display.set_caption('Парные картинки') #устанавливаем название окна
screen = display.set_mode((SCREEN_SIZE, SCREEN_SIZE)) #создаем игровое окно заданного размера (ширина и высота равны gc.SCREEN_SIZE)
matched = image.load('other_assets/matched.png') #загружаем изображение для использования при обнаружении совпавших картинок
running = True #устанавливаем флаг running, показывающий, что игра запущена и должна продолжаться
tiles = [Animal(i) for i in range(0, NUM_TILES_TOTAL)] #создаем список объектов класса Animal для всех элементов игры (картинок), используя цикл
current_images_displayed = []  #инициализация списка, в котором будут храниться текущие отображенные на экране картинки

while running: #запускаем бесконечный цикл, который будет выполняться до тех пор, пока флаг running установлен в True
    current_events = event.get() #получаем текущие события (например, нажатия клавиш, клики мыши) из очереди событий в pygame

    for e in current_events: #проходим по каждому событию из текущих событий
        if e.type == pygame.QUIT: #если тип события - выход из игры (нажатие крестика в окне)
            running = False #устанавливаем флаг running в False, чтобы выйти из игрового цикла

        if e.type == pygame.KEYDOWN: #если тип события - нажатие клавиши на клавиатуре
            if e.key == pygame.K_ESCAPE: #если нажата клавиша ESCAPE на клавиатуре
                running = False

        if e.type == pygame.MOUSEBUTTONDOWN: #если тип события - нажатие на мышь
            mouse_x, mouse_y = pygame.mouse.get_pos() #получаем текущие координаты мыши
            row, col, index = find_index_from_xy(mouse_x, mouse_y) #находим индекс элемента по координатам мыши
            if index not in current_images_displayed: #если данный элемент не отображается на экране
                if len(current_images_displayed) > 1: #если в списке отображенных элементов больше одного
                    current_images_displayed = current_images_displayed[1:] + [index] #удаляем первый элемент из списка отображенных элементов и добавляем новый элемент
                else:
                    current_images_displayed.append(index) #добавляем новый элемент в список отображения

    screen.fill((255, 255, 255)) #заполняем экран белым цветом, чтобы очистить старое содержимое перед отображением новых элементов

    total_skipped = 0 #инициализируем переменную total_skipped для подсчёта числа пропущенных плиток

    for i, tile in enumerate(tiles): #начинаем цикл по всем элементам списка tiles с использованием функции enumerate, чтобы иметь доступ как к индексу, так и к значению элемента
        current_image = tile.image if i in current_images_displayed else tile.box #определяем текущее изображение для отрисовки плитки в зависимости от того, должно ли оно быть отображено (tile.image) или скрыто (tile.box)
        if not tile.skip: #если плитка не пропущена (не найдена пара)
            screen.blit(current_image, (tile.col * IMAGE_SIZE + MARGIN, tile.row * IMAGE_SIZE + MARGIN)) #отображаем текущее изображение плитки на экране с учетом позиции плитки
        else:
            total_skipped += 1 #увеличиваем счётчик пропущенных плиток

    display.flip() #обновляем экран для отображения всех изменений в графике

    #Проверяем совпадения между выбранными плитками
    if len(current_images_displayed) == 2: #Если выбраны две плитки
        idx1, idx2 = current_images_displayed #распаковываем индексы двух выбранных элементов для удобства доступа к ним
        if tiles[idx1].name == tiles[idx2].name: #Псравниваем имена плиток (их идентификаторы), чтобы убедиться, что они одинаковые и совпадают
            tiles[idx1].skip = True #устанавливаем флаг skip в True для обеих плиток, чтобы они были помечены как найденные и могли быть "пропущены"
            tiles[idx2].skip = True
            
            sleep(0.2)  #ждем небольшой промежуток времени (0.2 секунды) перед отображением сообщения об успешном совпадении
            screen.blit(matched, (0, 0)) #отображаем изображение matched (сообщение о совпадении)
            display.flip() #обновляем экран, чтобы увидеть сообщение о совпадении
            sleep(0.5) #продолжаем отображать сообщение о совпадении в течение 0.5 секунды перед очисткой отображаемых изображений
            current_images_displayed = [] #очищаем список current_images_displayed, чтобы снова можно было выбрать две плитки для проверки на совпадение

    if total_skipped == len(tiles): #проверяем, если все плитки были пропущены (все имеют флаг skip)
        running = False #устанавливаем флаг running в False, чтобы завершить игровой цикл, так как все плитки найдены и закончен игровой процесс
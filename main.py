import os
import shutil
import requests
from get_coords import get_coords
from random import choice, randrange
import pygame
from config import SERVER_ADDRESS

if os.path.exists('photos'):
    shutil.rmtree('photos')

cities = ['Москва', 'Нью-Йорк', 'Владивосток', 'Париж', "Кэмбридж"]
os.mkdir('photos')
images = []
for i, city in enumerate(cities):
    city_coords = list(get_coords(city))
    lon_delta, lat_delta = randrange(20, 30) / float(1000), randrange(20, 30) / float(1000)
    lonlat = ','.join([str(float(city_coords[0]) + lon_delta), str(float(city_coords[1]) + lon_delta)])
    size = randrange(5, 30) / float(1000)
    params = {"ll": lonlat,
              "spn": f'{size},{size}',
              "l": choice(['map', 'sat'])}
    response = requests.get(SERVER_ADDRESS, params=params)
    filename = os.path.join('photos', f'{i}.png')
    file = open(filename, mode='wb')
    file.write(response.content)
    file.close()
    images.append(pygame.image.load(filename))
    del file

pygame.init()
pygame.display.set_caption('Угадай-ка город')
screen = pygame.display.set_mode((600, 450))
running = True
image = choice(images)
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]:
            prev_image = image
            while prev_image == image:
                image = choice(images)
    screen.fill('white')
    screen.blit(image, (0, 0))
    pygame.display.flip()
    clock.tick(24)
pygame.quit()

shutil.rmtree('photos')

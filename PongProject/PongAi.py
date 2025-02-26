import pygame
pygame.init()

from PongProject import main
from PongProject import handle_collision
from PongProject import handle_paddle_movement
from PongProject import Paddle
from PongProject import Ball

width,height = 700,500 
window = pygame.display.set_mode((width,height))

main = main()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
            break
    
    main.loop()
    main.draw(False, True)
    pygame.display.update()
    
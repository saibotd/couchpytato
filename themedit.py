#!/usr/bin/python

import pygame, os, time, sys
from pygame.locals import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        import cfg
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(cfg.thpath('thing.jpg')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(200,200))
        w,h = self.image.get_size(self.image)
        self.size = w,h
        self.rect = 0,0,w,h
        self.moveX = 0
        self.moveY = 0
        
    def update(self):
        if self.moveX != 0:
            self.rect = self.rect[0]+self.moveX, self.rect[1], self.rect[2], self.rect[3]
            self.moveX = 0
        if self.moveY != 0:
            self.rect =  self.rect[0], self.rect[1]+self.moveY, self.rect[2], self.rect[3]
            self.moveY = 0
        if self.size != self.rect[2:]:
            self.image = pygame.transform.scale(self.image, (self.size))
            self.rect = self.rect[0], self.rect[1], self.size[0], self.size[1]

class couchpytato:
    def __init__(self):

        pygame.init()
        import cfg
        resx = int(cfg.th['resolution'][0])
        resy = int(cfg.th['resolution'][1])
        pygame.display.set_caption('couchpytato') 
        pygame.display.set_icon(pygame.image.load(os.path.join(sys.path[0], 'icon.png')))
        screen = pygame.display.set_mode((resx, resy))
        bg = pygame.image.load(cfg.thpath('mainmenubg.png'))
        screen.blit(bg,(0,0))
        thing = Sprite()
        sprites = pygame.sprite.RenderUpdates((thing))
        pygame.display.update()
        pygame.mouse.set_visible(False)
        pygame.event.set_blocked(MOUSEMOTION)
        pygame.key.set_repeat(200, 80)
        clock = pygame.time.Clock()
        
        while 1:
            clock.tick(30)
            thing.update()
            pygame.display.update(sprites.draw(screen))
            sprites.clear(screen, bg)
            for event in pygame.event.get((KEYDOWN, KEYUP, QUIT)):
                if event.type == QUIT:
                    self.quit()
                if event.type == KEYDOWN:
                    if event.key == K_DOWN: thing.moveY += 10
                    if event.key == K_UP: thing.moveY -= 10
                    if event.key == K_LEFT: thing.moveX -= 10
                    if event.key == K_RIGHT: thing.moveX += 10
                    if event.key == K_s: thing.moveY += 1
                    if event.key == K_w: thing.moveY -= 1
                    if event.key == K_a: thing.moveX -= 1
                    if event.key == K_d: thing.moveX += 1
                    if event.key == K_i: thing.size = thing.size[0], thing.size[1]+1
                    if event.key == K_k: thing.size = thing.size[0], thing.size[1]-1
                    if event.key == K_j: thing.size = thing.size[0]-1, thing.size[1]
                    if event.key == K_l: thing.size = thing.size[0]+1, thing.size[1]
                    if event.key == K_SPACE: print thing.rect
                                   
    def quit(self):
        pygame.quit()
        sys.exit()
        
couchpytato()

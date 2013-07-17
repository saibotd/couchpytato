#!/usr/bin/env python

try:
    # trying to import 'psyco' which precompiles
    # the program in order to make it faster
    # [http://psyco.sourceforge.net/]
    import psyco
    psyco.full()
except ImportError:
    pass

import pygame, os, time, sys, configobj
from pygame.locals import *
sys.path.append(os.path.join(sys.path[0], "data"))

class couchpytato:
    def __init__(self):
        cf = configobj.ConfigObj(os.path.join(sys.path[0], 'couchpytato.cfg'))
        if cf['sound'] == 'pysonic':
            import pySonic
            w = pySonic.World()
        screen = self.init()
        import playlist, cfg, globals
        clock = pygame.time.Clock()
        
        joystick = None
        if pygame.joystick.get_init():
            print 'yes'
            print pygame.joystick.get_count()
            if pygame.joystick.get_count() > 0:
                joystick = pygame.joystick.Joystick(0)
                joystick.init()
                print joystick.get_name()
        mod = __import__('mod_mainmenu')
        pytato = mod.Module(screen)
        playlist.PLAYLIST.load()
        cnt = 0
        while 1:
            if globals.launchexapp:
                print 'display killed'
                playlist.PLAYLIST.pause()
                pygame.display.quit()
                os.system(globals.launchexapp)
                screen = self.init()
                pytato.screen = screen
                pytato.screen.blit(pytato.bg,(0,0))
                pygame.display.update()
                globals.launchexapp = None
                playlist.PLAYLIST.playpause()
            else:
                pytato.runloop()
                clock.tick(int(cfg.cf['fps']))
                cnt += 1
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.quit()
                    if pytato.loadmodule:
                        mod = __import__(pytato.loadmodule)
                        pytato = mod.Module(screen)
                    pytato.keyhandler(event)
                    pytato.generalkeyhandler(event)
                if joystick: pytato.joyhandler(joystick, cnt)
    
    def quit(self):
        import playlist
        playlist.PLAYLIST.save()
        pygame.quit()
        sys.exit()
    
    def init(self):
        pygame.init()
        import cfg
        resx = int(cfg.th['resolution'][0])
        resy = int(cfg.th['resolution'][1])
        pygame.display.set_caption('couchpytato') 
        pygame.display.set_icon(pygame.image.load(os.path.join(sys.path[0], 'icon.png')))
        if cfg.cf['fullscreen'] == '1':
            screen = pygame.display.set_mode((resx, resy),pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((resx, resy))
        pygame.mouse.set_visible(False)
        pygame.event.set_blocked(MOUSEMOTION)
        pygame.key.set_repeat(200, 80)
        return screen
        
couchpytato()

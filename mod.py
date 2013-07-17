import pygame, string, os, gui, cfg, time, playlist, globals
from pygame.locals import *

class Module:
    def __init__(self, screen):
        self.screen = screen
        self.gui = {}
        self.loop = {}
        self.addloop('UPDATE', self._updatesprites)
        self.layer = []
        self.loadmodule = None
        for g in range(10):
            self.layer.append(pygame.sprite.RenderUpdates())
        try:
            self.bg = pygame.image.load(cfg.thpath(globals.modulename + '_bg.png'))
        except:
            self.bg = pygame.image.load(cfg.thpath('bg.png'))
        self.screen.blit(self.bg,(0,0))
        pygame.display.update()
        #time.strftime(self.cf.val['config.dateformat'],time.localtime())
        for element in cfg.getgui(globals.modulename):
            self.addgui(element)
        self.addloop('UPDATECLOCK', self._updateclock)
        self.addloop('UPDATECURRENT', self._updatecurrent)
        self.addloop('AUTONEXT', self._autonext)
        self.init()
     
    def init(self):  #'real' init for the (child)modules. add guiobjects and loopevents here
        pass
        
    def keyhandler(self, event):
        pass

    def joyhandler(self, joystick, cnt):
        pass
        
    def generalkeyhandler(self, event):
        if event.type == KEYDOWN:
            if event.key == K_a: playlist.PLAYLIST.prev()
            if event.key == K_d: playlist.PLAYLIST.next()
            if event.key == K_s: playlist.PLAYLIST.playpause()
            if event.key == K_w: playlist.PLAYLIST.stop()
            if event.key == K_q: playlist.PLAYLIST.shuffle()
            if event.key == K_k: self._showcase()
            

    def showgeneralgui(self):
        for element in cfg.getgui('general'):
            self.addgui(element)

    def _updateclock(self):
        self.changebykey('CLOCK', time.strftime(cfg.cf['datetime'],time.localtime()))
        
    def _updatecurrent(self):
        if playlist.PLAYLIST.out.playing:
            self.changebykey('CURRENT', playlist.PLAYLIST.track(True))
            self.changebykey('PLAYTIME', playlist.PLAYLIST.time())
            inp = os.listdir(os.path.split(playlist.PLAYLIST.track())[0])
            image = cfg.thpath('blank.png')
            for line in inp:
                if line[-3:].lower() == 'jpg':
                    image = os.path.join(os.path.split(playlist.PLAYLIST.track())[0], line)
            self.changebykey('COVER', image)

    def addgui(self, guiobject):
        self.gui[guiobject.name] = guiobject
        if guiobject.typ == 'List':
            for label in guiobject.labels:
                self.layer[guiobject.layer].add(label)
            self.layer[guiobject.bar.layer].add(guiobject.bar)
        else:
            self.layer[guiobject.layer].add(guiobject)
        
    def removegui(self, name):
        if self.gui[name].typ == 'List':
            for label in self.gui[name].labels:
                self.layer[self.gui[name].layer].remove(label)
            if self.gui[name].bar:
                self.layer[self.gui[name].bar.layer].remove(self.gui[name].bar)
        else:
            self.layer[self.gui[name].layer].remove(self.gui[name])
        del self.gui[name]

    def addloop(self, name, loopaction):
        self.loop[name] = loopaction
    
    def removeloop(self, name):
        del self.loop[name]
    
    def runloop(self):
        for action in self.loop.values():
            action()

    def changebykey(self, contentkey, newcontent):
        for element in self.gui.values():
            if element.contentkey == contentkey:
                element.change = newcontent

    def _updatesprites(self):
        for guiobject in self.gui.values():
            if guiobject.visible:
                guiobject.update()
                
        rectlist = []
        for layer in self.layer:
            rectlist.extend(layer.draw(self.screen))
        pygame.display.update(rectlist)
        for layer in self.layer:
            layer.clear(self.screen, self.bg)

    def _autonext(self):
        if playlist.PLAYLIST.isplaying() == False and playlist.PLAYLIST.out.playing:
            playlist.PLAYLIST.next()

    def quit(self):
        pass

    def _showcase(self):
        self.quit()
        self.loadmodule = 'mod_showcase'
                

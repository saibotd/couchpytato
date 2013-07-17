import gui, pygame, os, time, mod, cfg, globals, key
from pygame.locals import *

class Module(mod.Module):
    def __init__(self, screen):
        globals.modulename = 'mod_mainmenu'
        mod.Module.__init__(self, screen)
        print globals.modulename
        i = 0
        for module in cfg.cf['modules'].values():
            self.gui['LIST'].add(module['title'], cfg.cf['modules'].keys()[i], self.loadmod, self.showicon)
            i += 1
        self.gui['LIST'].makelist()
        globals.val = {}
        globals.lastmodname = 'mod_mainmenu'
        self.showgeneralgui()
        
    def quit(self):
        globals.lastmodname = 'mod_mainmenu'
    
    def showicon(self, value):
        #if os.path.isfile(cfg.thpath(cfg.cf['modules'][value]['prefix'] + '_icon.png')):
        #    self.changebykey('ICON', cfg.thpath(cfg.cf['modules'][value]['prefix'] + '_icon.png'))
        #else:
        self.changebykey('ICON', cfg.thpath('blank.png'))

    def loadmod(self, value):
        i = 0
        for thing in cfg.cf['modules'][value].values():
            globals.val[cfg.cf['modules'][value].keys()[i]] = thing
            i += 1
        self.loadmodule = globals.get('modfilename')

    def keyhandler(self, event):
        if event.type == KEYDOWN:
            if event.key == K_DOWN: self.gui['LIST'].select_next()
            if event.key == K_UP: self.gui['LIST'].select_last()
            if event.key == K_RETURN: self.gui['LIST'].press()
            if event.key == key.right: self.gui['LIST'].press()

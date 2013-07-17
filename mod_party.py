import gui, pygame, os, time, mod_showcase, cfg, playlist, globals
from pygame.locals import *

class Module(mod_showcase.Module):
    def __init__(self, screen):
        globals.modulename = 'mod_showcase'
        mod_showcase.Module.__init__(self, screen)
        self.filetypes = globals.val['filetypes']
        self.path = globals.val['path']
        playlist.PLAYLIST.super_add(self.path, self.filetypes, False)
        playlist.PLAYLIST.shuffle()

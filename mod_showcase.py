import gui, pygame, os, time, mod, cfg, globals, playlist
from pygame.locals import *

class Module(mod.Module):
    def __init__(self, screen):
        globals.modulename = 'mod_showcase'
        mod.Module.__init__(self, screen)
        self.addloop('PlaylistUpdate', self._listupd)

    def keyhandler(self, event):
        if event.type == KEYDOWN:
            if event.key == K_LEFT: self.quit()
            if event.key == K_ESCAPE: self.quit()
            if event.key == K_UP: playlist.PLAYLIST.prev()
            if event.key == K_DOWN: playlist.PLAYLIST.next()
            
    
    def quit(self):
        self.loadmodule = globals.lastmodname

    def _listupd(self):
        import playlist
        self.changebykey('PLAYLIST-5', playlist.PLAYLIST.track(True, -5))
        self.changebykey('PLAYLIST-4', playlist.PLAYLIST.track(True, -4))
        self.changebykey('PLAYLIST-3', playlist.PLAYLIST.track(True, -3))
        self.changebykey('PLAYLIST-2', playlist.PLAYLIST.track(True, -2))
        self.changebykey('PLAYLIST-1', playlist.PLAYLIST.track(True, -1))
        self.changebykey('PLAYLIST+1', playlist.PLAYLIST.track(True, 1))
        self.changebykey('PLAYLIST+2', playlist.PLAYLIST.track(True, 2))
        self.changebykey('PLAYLIST+3', playlist.PLAYLIST.track(True, 3))
        self.changebykey('PLAYLIST+4', playlist.PLAYLIST.track(True, 4))
        self.changebykey('PLAYLIST+5', playlist.PLAYLIST.track(True, 5))

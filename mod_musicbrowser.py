import gui, pygame, os, time, mod_filebrowser, playlist, cfg
from pygame.locals import *

class Module(mod_filebrowser.Module):
    def __init__(self, name, screen):
        mod_filebrowser.Module.__init__(self, name, screen)
    
    def preinit(self):
        filetypes = ['mp3','ogg','wav']
        self.data = []
        self.path = cfg.cf['modules'][self.name]['path']
        for file in os.listdir(self.path):
            if os.path.isdir(os.path.join(self.path, file)):
                self.data.append(file)
            else:
                for ft in filetypes:
                    if file[-3:].lower() == ft:
                        self.data.append(file)
        self.data.sort()    
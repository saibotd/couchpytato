import mod, lib, os, cfg, pygame, globals
from pygame.locals import *

class Module(mod.Module):
    def __init__(self, screen):
        globals.modulename = 'mod_imageviewer'
        mod.Module.__init__(self, screen)
        path = globals.val['path']
        file = None
        if os.path.isfile(path):
            self.path, file = os.path.split(path)
        else:
            self.path = path
        self.files = []
        for files in os.listdir(self.path):
            if lib.ispic(os.path.join(self.path, files)):
                self.files.append(files)
        self.files.sort(key=str.lower)
        #self.pos = globals.val['history'].values()[-1][0] + globals.val['history'].values()[-1][1]
        self.pos = self.files.index(os.path.split(globals.val['file'])[1])
        self.changebykey('IMAGE', os.path.join(self.path, self.files[self.pos]))

    def keyhandler(self, event):
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                if self.pos < len(self.files)-1:
                    self.pos += 1
                else:
                    self.pos = 0
                self.changebykey('IMAGE', os.path.join(self.path, self.files[self.pos]))
            if event.key == K_UP:
                if self.pos > 0:
                    self.pos -= 1
                else:
                    self.pos = len(self.files)-1
                self.changebykey('IMAGE', os.path.join(self.path, self.files[self.pos]))
            if event.key == K_ESCAPE:
                self.loadmodule = globals.lastmodname

    def changebykey(self, contentkey, newcontent):
        for element in self.gui.values():
            if element.contentkey == contentkey:
                element.image = pygame.image.load(newcontent).convert_alpha()
                newrect = self._imgcalc(element.image, int(cfg.th['resolution'][0]), int(cfg.th['resolution'][1]))
                element.image = pygame.transform.scale(element.image, (newrect[2], newrect[3]))
                element.xpos, element.ypos = newrect[0], newrect[1]
                element.rect = newrect
    
    def _imgcalc(self, image, x, y):
        w, h = image.get_size()
        if w > x or h > y:
            if w >= h:
                d = float(w)/float(x)
                h = round(h/d)
                w = x
            elif w < h:
                d = float(h)/float(y)
                w = round(w/d)
                h = y
        posx = (x/2) - (w/2)
        posy = (y/2) - (h/2)
        return int(posx), int(posy), int(w), int(h)

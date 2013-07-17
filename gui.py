import pygame, os, random, string, cfg
from pygame.locals import *

# GuiObject is everything (pictures, labels...) you see on the gui

class GuiObject(pygame.sprite.Sprite):
    def __init__(self, name, xpos, ypos, layer):
        pygame.sprite.Sprite.__init__(self)
        self.typ = 'Parent'
        self.xpos = xpos
        self.ypos = ypos
        self.name = name
        self.layer = layer
        self.image = None
        self.rect = xpos,ypos,0,0
        self.change = None
        self.fx = None
        self.fxspeed = 1
        self.visible = True
        self.contentkey = None
        self.contentkeyarg = None

    def update(self):
        if self.fx:
            if self.fx[0] == 's':
                self.effects()
        if self.xpos != self.rect[0] or self.ypos != self.rect[1]:
            if self.fx and cfg.cf['disablefx'] == '0':
                if self.fx[0] == 'm':
                    self.effects()
            else:
                self.rect = self.xpos, self.ypos, self.rect[2], self.rect[3]
        if self.change:
            self._changeimage()
    
    def _makeimage(self):
        pass

    def _changeimage(self):
        pass
    
    def effects(self):
        if self.fx == 'm_slide':
            x = self.rect[0]
            y = self.rect[1]
            if self.ypos != y:
                if self.ypos < y:
                        y -= self.fxspeed

                elif self.ypos > y:
                        y += self.fxspeed
            self.rect = x, y, self.rect[2], self.rect[3]
            
        if self.fx == 's_scroll':
            text = self.orgtext
            if text == None:
                text = ' '
            if self.font.size(text)[0] > int(self.width):
                image = self.font.render(text, 1, self.color)
                w, h = image.get_size()
                orgwidth = w
                choprect = 0, h, self.scrollcount, h
                image = pygame.transform.chop(image, choprect)
                choprect = self.width, h, int(cfg.th['resolution'][0]), h
                image = pygame.transform.chop(image, choprect)
                self.image = image.convert_alpha()
                w, h = self.image.get_size()
                self.rect = self.rect[0], self.rect[1], w, h
                if orgwidth < self.width + self.scrollcount:
                    self.scrollinv = True
                elif self.scrollcount == 0:
                    self.scrollinv = False
                if self.scrollinv: self.scrollcount -= self.fxspeed
                else: self.scrollcount += self.fxspeed

class Image(GuiObject):
    def __init__(self, name, xpos, ypos, layer, imagefile, size=None, alpha=None, hflip=False, vflip=False, degree=None):
        GuiObject.__init__(self, name, xpos, ypos, layer)
        self.typ = 'Image'
        self.alpha = alpha
        self.size = size
        self.hflip = hflip
        self.vflip =vflip
        self.degree = degree
        self.imagefile = imagefile
        self._makeimage()
        
    def _makeimage(self):
        self.image = pygame.image.load(self.imagefile)
        self.image = pygame.transform.flip(self.image, self.hflip, self.vflip)
        if self.size: self.image = pygame.transform.scale(self.image, (self.size, self.size))
        if self.alpha: self.image.set_alpha(self.alpha)
        if self.degree: self.image = pygame.transform.rotate(self.image, self.degree)
        self.image = self.image.convert_alpha()
        w,h = self.image.get_size()
        self.rect = self.xpos, self.ypos, w, h

    def _changeimage(self):
        if self.change:
            if self.imagefile != self.change:
                oldimagefile = self.image
                self.imagefile = self.change
                try:
                    self._makeimage()
                except:
                    self.imagefile = oldimagefile
            self.change = None

class ListBar(Image):
    def __init__(self, name, xpos, ypos, layer, imagefile, xoff, yoff):
        Image.__init__(self, name, xpos+xoff, ypos+yoff, layer, imagefile)
        self.xoff = xoff
        self.yoff = yoff

class Label(GuiObject):
    def __init__(self, name, xpos, ypos, layer, font, (r,g,b), text=' ', width=None, extra=None):
        GuiObject.__init__(self, name, xpos, ypos, layer)
        self.typ = 'Label'
        self.font = font
        self.orgtext = text
        self.text = text
        self.color = (r,g,b)
        self.width = width
        self.extra = extra
        self.scrollcount = 0
        self.scrollinv = False
        self._makeimage()
        
    def _makeimage(self):
        if self.width:
            while self.font.size(self.text)[0] > self.width:
                self.text = self.text[0:-1]
        if self.extra and self.text != ' ':
            self.text = self.text + self.extra
        self.image = self.font.render(str(self.text), int(cfg.cf['fontaa']), self.color)
        self.image = self.image.convert_alpha()

    def _changeimage(self):
        if self.change:
            if self.orgtext != self.change:
                self.orgtext = self.change
                self.text = self.change
                self.scrollcount = 0
                self.scrollinv = False
                self._makeimage()
        
# self.font = pygame.font.Font(ttf, int(size))

class List:
    def __init__(self, name, xpos, ypos, layer, font, (r,g,b), maxlen, space, width, listbar):
        self.name = name
        self.xpos = xpos
        self.ypos = ypos
        self.layer = layer
        self.typ = 'List'
        self.maxlen = maxlen
        self.space = space
        self.font = font
        self.visible = True
        self.color = (r,g,b)
        self.sprites = []
        self.bar = listbar
        self.bar.fx = 'm_slide'
        self.bar.fxspeed = space/2
        self.selected = 0
        self.liststart = 0
        self.list = []
        self.labels = []
        self.width = width
        self.contentkey = None
        self.contentkeyarg = None
        for g in range(self.maxlen):
            y = g*self.space+self.ypos
            self.labels.append(Label('lbl'+str(g), self.xpos, y, self.layer, self.font, self.color, ' ', self.width))
        self.curvalue = None

    def update(self):
        for label in self.labels:
            label.update()
        if self.bar:
            self.bar.update()
    
    def press(self):
        self.list[self.liststart + self.selected].press()
    
    def clear(self):
        self.liststart = 0
        self.selected = 0
        self.list = []
        #self.makelist()
    
    def add(self, text, value, onpress, onselect):
        self.list.append(ListItem(text, value, onpress, onselect))
    
    def makelist(self):
        if self.selected < 0: self.selected = 0
        if self.liststart < 0: self.liststart = 0
        if self.liststart + self.selected > len(self.list)-1:
            self.liststart = 0
            self.selected = 0
        if len(self.list[self.liststart:]) < self.maxlen:
            for i in range(self.maxlen - len(self.list[self.liststart:])):
                self.labels[i+len(self.list[self.liststart:])].change = ' '
        self._updbar(True)
                
        i = 0
        for item in self.list[self.liststart:]:
            self.labels[i].change = item.text
            i += 1
            if i == self.maxlen: break
        self.list[self.liststart + self.selected].select()

    def _updbar(self, straight=False):
        if straight:
            self.bar.rect = self.bar.rect[0],self.selected * self.space + (self.ypos + self.bar.yoff),self.bar.rect[2],self.bar.rect[3]
        self.bar.ypos = self.selected * self.space + (self.ypos + self.bar.yoff)
        for line in self.labels: #!!!!!!
            line.fx = None
        self.list[self.liststart + self.selected].select()
        self.labels[self.selected].fx = 's_scroll'
        self.labels[self.selected].fxspeed = 2
    
    def select_next(self):
        if self.selected < self.maxlen -1 and self.liststart+self.selected < len(self.list)-1:
            self.selected += 1
            self._updbar()
        else:
            self.next_page()

    def select_last(self):
        if self.selected > 0:
            self.selected -= 1
            self._updbar()
        else:
            self.last_page()

    def next_page(self):
        self.selected = 0
        if self.liststart > len(self.list) - self.maxlen:
            self.liststart = 0
        else:
            self.liststart += self.maxlen
        self.makelist()

    def last_page(self):
        if len(self.list) < self.maxlen:
            self.selected = len(self.list)-1
        else:
            self.selected = self.maxlen-1
        if self.liststart == 0:
            self.liststart = len(self.list)-self.maxlen
        else:
            self.liststart -= self.maxlen
        self.makelist()
        
        

class ListItem:
    def __init__(self, text, value, onpress, onselect):
        self.text = text
        if os.path.isdir(value):
            self.text = '[' + text + ']'
        elif os.path.isfile(value):
            self.text, ext = os.path.splitext(text)
        self.value = value
        self.pressaction = onpress
        self.selectaction = onselect
    
    def press(self):
        return self.pressaction(self.value)
    
    def select(self):
        return self.selectaction(self.value)

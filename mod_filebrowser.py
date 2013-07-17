import gui, pygame, os, time, mod, playlist, cfg, random, lib, globals
from pygame.locals import *

class Module(mod.Module):
    def __init__(self, screen):
        globals.modulename = 'mod_filebrowser'
        mod.Module.__init__(self, screen)
        self.filetypes = '*'
        if globals.get('filetypes'): self.filetypes = globals.get('filetypes')
        self.path = '/'
        if globals.get('path'): self.path = globals.get('path')
        self.action = 'SHOW_IMAGE'
        if globals.get('action'): self.action = globals.get('action')
        self._path = self.path
        self.history = {}
        if globals.get('history'): self.history = globals.get('history')
        self.filllist()
        self.prevcnt = 0
        self.history[self.path] = 0,0
        self.addloop('previewimg', self._prevwait)
        self.showgeneralgui()
        self.depth = 0
        if globals.get('depth'): self.depth = globals.get('depth')
        self.joyreset = True
        self.waitframes = 0
        self.waitaction = None
        self.joyscrollspeed = 8
        self.joyspeedcount = 0

    def quit(self):
        self.history[self.path] = self.gui['LIST'].liststart, self.gui['LIST'].selected
        globals.lastmodname = 'mod_filebrowser'
        globals.val['path'] = self.path
        globals.val['history'] = self.history
        globals.val['depth'] = self.depth

    def filllist(self):
        self.data = []
        print self.history
        try:
            self.gui['LIST'].liststart, self.gui['LIST'].selected = self.history[self.path]
        except:
            pass
        if self.filetypes == '*':
            self.data = os.listdir(self.path)
        else:
            for file in os.listdir(self.path):
                if os.path.isdir(os.path.join(self.path, file)):
                    self.data.append(file)
                else:
                    for ft in self.filetypes:
                        if file[-3:].lower() == ft:
                            self.data.append(file)
        self.data.sort(key=str.lower)
        if len(self.data) > 0:
            for file in self.data:
                self.gui['LIST'].add(file,os.path.join(self.path,file),self._action,self._prevtrig)
            self.gui['LIST'].makelist()
        else:
            self.path, d = os.path.split(self.path)
            self.depth -= 1

    def keyhandler(self, event):
        if event.type == KEYDOWN:
            if event.key == K_DOWN: self.gui['LIST'].select_next()
            if event.key == K_UP: self.gui['LIST'].select_last()
            if event.key == K_PAGEDOWN: self.gui['LIST'].next_page()
            if event.key == K_PAGEUP: self.gui['LIST'].last_page()
            if event.key == K_RIGHT:
                if os.path.isdir(self.sel_path):
                    self._updprev()
                    self.history[self.path] = self.gui['LIST'].liststart, self.gui['LIST'].selected
                    self.gui['LIST'].clear()
                    self.path = self.sel_path
                    self.filllist()
                    self.depth += 1
            if event.key == K_LEFT:
                if self.depth > 0:
                    self._updprev()
                    self.gui['LIST'].clear()
                    self.path, d = os.path.split(self.path)
                    self.filllist()
                    self.depth -= 1
                else:
                    globals.val['depth'] = 0
                    globals.val['history'] = {}
                    self.loadmodule = 'mod_mainmenu'
            if event.key == K_RETURN: 
                self.gui['LIST'].press()
            if event.key == K_y: playlist.PLAYLIST.super_add(self._path, self.filetypes)

    def joyhandler(self, joystick, cnt):
        tol0 = 0.5
        tol1 = tol0 - (tol0 * 2)
        if joystick.get_axis(0) > tol0 or joystick.get_axis(0) < tol1:
            if joystick.get_axis(0) > 0:
                pass
            elif joystick.get_axis(0) < 0:
                pass
        if joystick.get_axis(1) > tol0 or joystick.get_axis(1) < tol1:
            if joystick.get_axis(1) > 0:
                if self.joyreset:
                    self.gui['LIST'].select_next()
                    self.joyreset = False
                elif cnt % self.joyscrollspeed == 0:
                    self.gui['LIST'].select_next()
                    self.joyspeedcount += 1
                if self.joyspeedcount > 3:
                    self.joyscrollspeed = 2
            elif joystick.get_axis(1) < 0:
                if self.joyreset:
                    self.gui['LIST'].select_last()
                    self.joyreset = False
                elif cnt % self.joyscrollspeed == 0:
                    self.gui['LIST'].select_last()
                    self.joyspeedcount += 1
                if self.joyspeedcount > 3:
                    self.joyscrollspeed = 2
        elif self.joyreset == False:
            self.joyreset = True
            self.joyspeedcount = 0
            self.joyscrollspeed = 8
        if joystick.get_button(0):
            if os.path.isdir(self.sel_path):
                self._updprev()
                self.history[self.path] = self.gui['LIST'].liststart, self.gui['LIST'].selected
                self.gui['LIST'].clear()
                self.path = self.sel_path
                self.filllist()
                self.depth += 1

    def _resjoy(self):
        self.joyreset = True

    def _wait(self, frames, action):
        self.waitframes == frames
        self.waitaction = action
        self.addloop('_WAIT_', self._waitloop)
    
    def _waitloop(self):
        print self.waitframes
        self.waitframes -= 1
        if self.waitframes <= 0:
            self.removeloop('_WAIT_')
            self.waitaction
            self.waitaction = None
            self.waitframes = 0

    def _nut(self, value=None):
        pass

    def _action(self, value):
        if self.action == 'PLAY_MUSIC':
            if os.path.isdir(value):
                path = value
                playlist.PLAYLIST.add_dir(path, self.filetypes)
            elif os.path.isfile(value):
                path, fil = os.path.split(value)
                playlist.PLAYLIST.add_dir(path, self.filetypes, self.gui['LIST'].liststart + self.gui['LIST'].selected)
            self.quit()
            self.loadmodule = 'mod_showcase'
        elif self.action == 'SHOW_PICTURE':
            globals.val['file'] = value
            self.quit()
            self.loadmodule = 'mod_imageviewer'
        else:
            # pygame stops. This was mainly necessary for ZSNES, which doesn't start with running
            # pygame display, also it saves a lot cpu-time for the launched application
            
            # quitting the display
            globals.launchexapp = self.action + ' "' + value + '"'
            # launching the application with filename parameters
            # bringing up the display again

    def _updprev(self):
        if os.path.isdir(self.previmage):
            inp = os.listdir(self.previmage)
            image = cfg.thpath('blank.png')
            imagepool = []
            for line in inp:
                if lib.ispic(os.path.join(self.previmage, line)):
                    #image = os.path.join(self.previmage, line)
                    imagepool.append(os.path.join(self.previmage, line))
            if len(imagepool) > 0:
                num = random.randint(0, len(imagepool)-1)
                image = imagepool[num]
            self.changebykey('PREVIEW', image)
        elif lib.ispic(self.previmage):
            self.changebykey('PREVIEW', self.previmage)

    def _prevwait(self):
        self.prevcnt += 1
        if self.prevcnt == 15:
            self._updprev()
    
    def _prevtrig(self, value):
        self.sel_path = os.path.join(self.path, value)
        self.previmage = value
        self.prevcnt = 0

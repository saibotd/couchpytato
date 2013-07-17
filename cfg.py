import configobj, os, gui, pygame, sys

cf = configobj.ConfigObj(os.path.join(sys.path[0], 'couchpytato.cfg'))
th = configobj.ConfigObj(os.path.join(sys.path[0], 'themes', cf['theme'], 'theme.cfg'))

def thpath(file):
    return os.path.join(sys.path[0], 'themes', cf['theme'], file)

fonts = {}
for i in range(len(th['fonts'].values())):
    font = th['fonts'].values()[i]
    ttf = thpath(font[0])
    size = int(font[1])
    fonts[th['fonts'].keys()[i]] = pygame.font.Font(ttf, size)

def getgui(module):
    GUI = []
    i = 0
    for obj in th[module].values():
        name = th[module].keys()[i]
        xpos = int(obj['xpos'])
        ypos = int(obj['ypos'])
        layer = int(obj['layer'])
        try:
            contentkey = obj['contentkey']
        except:
            contentkey = None
        try:
            fx = obj['fx'][0]
            fxspeed = int(obj['fx'][1])
        except:
            fx = None
            fxspeed = 1
        if obj['class'] == 'IMAGE':
            image = thpath(obj['image'])
            try:
                size = int(obj['size'])
            except:
                size = None
            try:
                alpha = int(obj['alpha'])
            except:
                alpha = None
            try:
                hflip = bool(obj['hflip'])
            except:
                hflip = False
            try:
                vflip = bool(obj['vflip'])
            except:
                vflip = False
            try:
                degree = int(obj['degree'])
            except:
                degree = None
            GUI.append(gui.Image(name, xpos, ypos, layer, image, size, alpha, hflip, vflip, degree))
        
        if obj['class'] == 'LABEL':
            font = fonts[obj['font']]
            color = int(obj['color'][0]), int(obj['color'][1]), int(obj['color'][2])
            try:
                text = obj['text']
            except:
                text = ' '
            try:
                width = int(obj['width'])
            except:
                width = None
            try:
                extra = obj['extra']
            except:
                extra = None
            GUI.append(gui.Label(name, xpos, ypos, layer, font, color, text, width, extra))
        
        if obj['class'] == 'LIST':
            barlayer = int(obj['barlayer'])
            barimage = thpath(obj['barimage'])
            xoff = int(obj['xoff'])
            yoff = int(obj['yoff'])
            listbar = gui.ListBar('bar', xpos, ypos, barlayer, barimage, xoff, yoff)
            color = int(obj['color'][0]), int(obj['color'][1]), int(obj['color'][2])
            maxlen = int(obj['maxlen'])
            space = int(obj['space'])
            width = int(obj['width'])
            GUI.append(gui.List(name, xpos, ypos, layer, fonts[obj['font']], color, maxlen, space, width, listbar))
        GUI[-1].contentkey = contentkey
        GUI[-1].fx = fx
        GUI[-1].fxspeed = fxspeed
        i += 1
        
    return GUI

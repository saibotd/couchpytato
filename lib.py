import os

def ispic(filename):
    ispic = False
    if os.path.isfile(filename):
        ext = filename[-3:].lower()
        if ext == 'jpg' or ext == 'gif' or ext == 'bmp' or ext == 'png' or ext == 'jpeg':
            ispic = True
    return ispic
import pySonic, time

class Music:
    def __init__(self):
        self.music = pySonic.Source()
        self.playing = False
        self.paused = False

    def isplaying(self):
        return self.music.IsPlaying()    
    
    def play(self, name=None):
        ok = True
        if self.paused:
            self.music.Play()
            self.playing = True
            self.paused = False
        elif name:
            try:
                self.music.Sound = pySonic.FileStream(name)
            except:
                ok = False
            if ok:
                self.music.Play()
                self.playing = True
                self.paused = False
        else:
            ok = False
        return ok
        
    def pause(self):
        if self.isplaying():
            self.music.Pause()
            self.playing = False
            self.paused = True
    
    def time(self, what=0):
        if self.isplaying():
            secs = int(self.music.CurrentTime)
            tim = time.localtime(secs)
            min = str(tim[4])
            sec = str(tim[5])
            if len(min) == 1:
                min = '0' + min
            if len(sec) == 1:
                sec = '0' + sec
            return min + ':' + sec
        else:
            return None
    
    def stop(self):
        if self.isplaying():
            self.music.Stop()
            self.playing = 0

import pygame.mixer, time

class Music:
	def __init__(self):
		self.playing = False
		self.paused = False
		pygame.mixer.init()

	def isplaying(self):
		return pygame.mixer.music.get_busy()
	
	def play(self, name=None):
		ok = True
		if self.paused:
			pygame.mixer.music.unpause()
			self.playing = True
			self.paused = False
		elif name:
			try:
				pygame.mixer.music.load(name)
			except:
				ok = False
			if ok:
				pygame.mixer.music.play()
				self.playing = True
				self.paused = False
		else:
			ok = False
		return ok
		
	def pause(self):
		if self.isplaying():
			pygame.mixer.music.pause()
			self.playing = False
			self.paused = True
	
	def time(self, what=0):
		if self.isplaying():
			secs = int(pygame.mixer.music.get_pos()/1000)
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
			pygame.mixer.music.stop()
			self.playing = 0

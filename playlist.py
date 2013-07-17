import os, sys, random, cfg

class Playlist:
	def __init__(self):
		sound = __import__(cfg.cf['sound'])
		self.tracks = []
		self.pos = 0
		self.out = sound.Music()
		self.playlistfile = os.path.join(sys.path[0], '.lastplayed.lst')

	def isplaying(self):
		return self.out.isplaying()
	
	def play(self):
		if self.tracks:
			if self.out.play(self.tracks[self.pos]):
				self.save()
			else:
				if len(self.tracks) != 1:
					self.tracks.remove(self.tracks[self.pos])
					self.play()
				else:
					self.stop()
		
	def pause(self):
		if self.isplaying:
			self.out.pause()

	def playpause(self):
		if self.out.paused:
			self.out.play()
		else:
			self.out.pause()
		return self.out.paused
	
	def time(self):
		if self.out.time():
			return self.out.time()
		else:
			return ' '
	
	def track(self, split=False, frompos=0):
	    txt = None
	    if len(self.tracks)>0:
	        if self.pos+frompos > len(self.tracks)-1:
	            frompos = frompos -len(self.tracks)
	        txt = self.tracks[self.pos+frompos]
            if split:
                trash, txt = os.path.split(txt)
                txt, trash = os.path.splitext(txt)
            return txt
	
	def stop(self):
		self.tracks = []
		self.pos = 0
		if self.out.isplaying():
			self.out.playing = False
			self.out.stop()
			if os.path.isfile(self.playlistfile):
				try:
					os.unlink(self.playlistfile)
				except OSError:
				    pass
	
	def next(self):
		if self.tracks:
			if self.pos == len(self.tracks) - 1:
				self.pos = 0
			else:
				self.pos = self.pos + 1
			self.play()
		
	def prev(self):
		if self.tracks:
			if self.pos == 0:
				self.pos = len(self.tracks) - 1
			else:
				self.pos = self.pos - 1
			self.play()
		
	def add(self, name):
		self.tracks.append(name)
		
	def add_dir(self, name, filetypes, selected=None, keep=False):
		old_tracks = self.tracks
		if keep == False:
			self.tracks = []
			self.pos = 0
		inp = os.listdir(name)
		for line in inp:
			(shortname, ext) = os.path.splitext(line)
			for lin in filetypes:
				if ext[1:] == lin:
					self.tracks.append(os.path.join(name, line))
					break
		self.tracks.sort(key=str.lower)  
		if self.tracks != [] and keep == False:
			if selected:
				self.pos=selected
			if self.out.isplaying():
				self.out.stop()
			self.play()
		else:
			self.tracks = old_tracks

	def super_add(self, name, filetypes, keep=False):
		old_tracks = self.tracks
		if keep == False:
			self.tracks = []
			self.pos = 0
		sadd = Superadd(name, filetypes)
		if sadd.files != [] and keep == False:
			self.tracks = sadd.files
			if self.out.isplaying():
				self.out.stop()
			self.play()
		else:
			self.tracks = old_tracks

	def shuffle(self):
		if self.tracks:
			self.out.stop()
			random.shuffle(self.tracks)
			self.pos = 0
			self.play()

	def save(self):
		if self.tracks:
			out_file = open(self.playlistfile,'w')
			out_file.write(str(self.pos) + '\n')
			for file in self.tracks:
				try:
					out_file.write(file + '\n')
				except:
					pass
			out_file.close()
		
	def load(self, file=None):
	    if file == None:
	        file = self.playlistfile
		if os.path.isfile(file):
			in_file = open(file,'r')
			self.tracks = []
			self.pos = 0
			i = 0
			for line in in_file:
				if i == 0 and file == self.playlistfile:
					self.pos = int(line)
				elif line[1] != '#':
					if os.path.isfile(line[:-1]):
						self.tracks.append(str(line[:-1]))
				i += 1
			if self.tracks:
				self.play()

class Superadd:
	def __init__(self, path, ft=None):
		self.files = []
		try:
			self.searchdir(path, ft)
		except:
			pass
	def searchdir(self, path, ft=None):
		for line in os.listdir(path):
			if os.path.isdir(os.path.join(path,line)):
				self.searchdir(os.path.join(path,line), ft)
			else:
				if ft:
					for ext in ft:
						(shortname, ex) = os.path.splitext(line)
						if ex[1:] == ext:
							self.files.append(os.path.join(path,line))
				else:
					self.files.append(os.path.join(path,line))
		return self.files.sort(key=str.lower)

PLAYLIST = Playlist()
launchexapp = None
modulename = None
val = {}

def get(var):
	try:
		return val[var]
	except:
		return None

import globals, mod
class Module(mod.Module):
    def __init__(self, screen):
        globals.launchexapp = '"' + globals.get('action') + '"'
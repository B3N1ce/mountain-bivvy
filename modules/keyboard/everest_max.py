import hid
from .mediadock import MediaDock
from .numpad import Numpad

class EverestMax:
    def __init__(self, vid=0x3282, pid=0x0001):
        self.vid = vid
        self.pid = pid
        self.device = None
        self.dock = None
        self.numpad = None

    def connect(self):
        try:
            for d in hid.enumerate(self.vid, self.pid):
                if d['interface_number'] == 3:
                    self.device = hid.device()
                    self.device.open_path(d['path'])
                    self.device.set_nonblocking(True)
                    
                    # Dependency Injection: Das Gerät an die Module übergeben
                    self.dock = MediaDock(self.device)
                    self.numpad = Numpad(self.device)
                    return True
            return False
        except Exception as e:
            print(f"Verbindungsfehler Everest Max: {e}")
            return False
            
    def disconnect(self):
        if self.device:
            self.device.close()
            self.device = None
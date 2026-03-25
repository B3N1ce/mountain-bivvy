import time
from .base import EverestModule

class MediaDock(EverestModule):
    def set_volume(self, volume):
        if not self.device:
            return
        
        # Deine geknackte Wireshark-Sequenz
        p1 = [0x00, 0x11, 0x14] + [0x00] * 62
        p2 = [0x00, 0x11, 0x83, 0x00, 0x00, volume] + [0x00] * 59
        
        try:
            self.device.write(p1)
            time.sleep(0.005)
            self.device.write(p2)
        except Exception as e:
            print(f"MediaDock Schreibfehler: {e}")
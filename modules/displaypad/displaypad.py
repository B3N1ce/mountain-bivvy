import hid
import json
import os
from . import displaypad_keyfunctions as kf

class DisplaypadKey:
    def __init__(self, index, byte_pos, bit_value, action=None):
        self.index = index
        self.byte_pos = byte_pos
        self.bit_value = bit_value
        self.state = 0  # 0 = losgelassen, 1 = gedrückt
        self.action = action

    def press(self):
        self.state = 1
        if self.action:
            self.action()

    def release(self):
        self.state = 0

class Displaypad:
    def __init__(self, vid=0x3282, pid=0x0009):
        self.vid = vid
        self.pid = pid
        self.device = None
        self.keys = {}
        self.config_path = "config.json"

    def connect(self):
        try:
            devices = hid.enumerate(self.vid, self.pid)
            target_path = next((d['path'] for d in devices if d['interface_number'] == 3), None)
            if target_path:
                self.device = hid.device()
                self.device.open_path(target_path)
                self.device.set_nonblocking(True)
                self.load_config_and_init_keys()
                return True
            return False
        except Exception as e:
            print(f"Displaypad Verbindungsfehler: {e}")
            return False

    def load_config_and_init_keys(self):
        # Lade JSON
        config_data = {"keys": {}}
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                config_data = json.load(f)

        # Byte/Bit Mapping aus deinem Prototyp
        mapping = [
            (1, 42, 2), (2, 42, 4), (3, 42, 8), (4, 42, 16), (5, 42, 32), (6, 42, 64),
            (7, 42, 128), (8, 47, 1), (9, 47, 2), (10, 47, 4), (11, 47, 8), (12, 47, 16)
        ]

        self.keys.clear()
        for idx, byte, bit in mapping:
            key_info = config_data["keys"].get(str(idx))
            action_func = None
            
            if key_info:
                func_name = key_info.get("action")
                # Nutze AVAILABLE_ACTIONS aus deinem Modul
                if hasattr(kf, 'AVAILABLE_ACTIONS') and func_name in kf.AVAILABLE_ACTIONS:
                    action_func = kf.AVAILABLE_ACTIONS[func_name]
                elif hasattr(kf, func_name): # Fallback auf direkten Funktionsnamen
                    action_func = getattr(kf, func_name)

            self.keys[idx] = DisplaypadKey(idx, byte, bit, action=action_func)

    def process_data(self, data):
        if not data: return
        for key in self.keys.values():
            is_pressed = (data[key.byte_pos] & key.bit_value) != 0
            if is_pressed and key.state == 0:
                key.press()
            elif not is_pressed and key.state == 1:
                key.release()
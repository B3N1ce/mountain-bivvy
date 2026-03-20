import hid
import time
import displaypad_keyfunctions as kf
import json

# Konfiguration
VENDOR_ID = 0x3282 #Mountain
PRODUCT_ID = 0x0009 # Displaypad
INTERFACE_NUM = 3

# globale Variablen
KEY_MAP = {} # Key Dictionary

class DisplaypadKey:
    def __init__(self, index, byte_pos, bit_value, action=None):
        self.index = index
        self.byte_pos = byte_pos
        self.bit_value = bit_value
        self.state = 0  # 0 = losgelassen, 1 = gedrückt
        self.action = action if action else self.empty

    def __repr__(self):
        # logging
        status = "PRESSED" if self.state == 1 else "RELEASED"
        return f"[Key {self.index:02d}] Status: {status:8s} (Byte:{self.byte_pos} Bit:{self.bit_value})"

    def empty(self):
        print("ACTION: empty")

    def press(self):
        self.state = 1
        # Hier könnte später die Logik stehen (z.B. ein Programm starten)
        print(f"DOWN: {self}") # Nutzt automatisch __repr__
        self.action()

    def release(self):
        self.state = 0
        print(f"UP:   {self}") # Nutzt automatisch __repr__

def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Config nicht gefunden, lade Defaults...")
        return {"keys": {}}

def init_keys():
    KEY_MAP.clear()
    config_data = load_config()
    # Index, Byte, BitValue
    mapping = [
        ( 1, 42,   2), ( 2, 42,   4), ( 3, 42,   8), ( 4, 42,  16), ( 5, 42,  32), ( 6, 42,  64), 
        ( 7, 42, 128), ( 8, 47,   1), ( 9, 47,   2), (10, 47,   4), (11, 47,   8), (12, 47,  16)
    ]
    
    for idx, byte, bit in mapping:
        # 1. Daten aus JSON holen
        key_info = config_data["keys"].get(str(idx))
        assigned_action = None
        
        if key_info:
            func_name = key_info.get("action")
            args = key_info.get("args", [])
            
            # 2. Funktion dynamisch im Modul 'kf' suchen
            if hasattr(kf, func_name):
                func = getattr(kf, func_name)
                # Falls Argumente da sind, nutzen wir lambda zum "Vorverpacken"
                if args:
                    assigned_action = lambda a=args, f=func: f(*a)
                else:
                    assigned_action = func
        
        KEY_MAP[idx] = DisplaypadKey(idx, byte, bit, action=assigned_action)

def process_usb_data(data):
    """Prüft alle Tasten-Objekte gegen das aktuelle USB-Paket."""
    for key in KEY_MAP.values():
        # Bitweise Prüfung: Ist das Bit im entsprechenden Byte gesetzt?
        is_pressed = (data[key.byte_pos] & key.bit_value) != 0
        
        # Flankenerkennung (nur bei Änderung loggen)
        if is_pressed and key.state == 0:
            key.press()
            
        elif not is_pressed and key.state == 1:
            key.release()

def main():
    init_keys()
    
    try:
        # Interface suchen
        devices = hid.enumerate(VENDOR_ID, PRODUCT_ID)
        target_path = next((d['path'] for d in devices if d['interface_number'] == INTERFACE_NUM), None)
        
        if not target_path:
            print(f"Fehler: Interface {INTERFACE_NUM} nicht gefunden!")
            return

        device = hid.device()
        device.open_path(target_path)
        # Device in den non-blocking Modus setzen, falls gewünscht, 
        # hier bleiben wir aber beim sauberen blocking read für den Logger.
        
        print(f"Erfolgreich verbunden mit Displaypad (IF {INTERFACE_NUM})")
        print("Überwachung gestartet. Drücke Tasten zum Testen (Strg+C zum Beenden).")
        print("-" * 60)

        while True:
            # Wir lesen 64 Bytes (Standard USB Report Größe)
            data = device.read(64)
            if data:
                process_usb_data(data)

    except KeyboardInterrupt:
        print("\nMonitoring beendet.")
    except Exception as e:
        print(f"\nEin Fehler ist aufgetreten: {e}")
    finally:
        if 'device' in locals():
            device.close()

if __name__ == "__main__":
    main()
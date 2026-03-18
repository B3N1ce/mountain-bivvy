import hid
import time

# Konfiguration
VENDOR_ID = 0x3282 #Mountain
PRODUCT_ID = 0x0009 # Displaypad
INTERFACE_NUM = 3

# globale Variablen
KEY_MAP = {} # Key Dictionary

class DisplaypadKey:
    def __init__(self, index, byte_pos, bit_value):
        self.index = index
        self.byte_pos = byte_pos
        self.bit_value = bit_value
        self.state = 0  # 0 = losgelassen, 1 = gedrückt

    def __repr__(self):
        # logging
        status = "PRESSED" if self.state == 1 else "RELEASED"
        return f"[Key {self.index:02d}] Status: {status:8s} (Byte:{self.byte_pos} Bit:{self.bit_value})"

    def press(self):
        self.state = 1
        # Hier könnte später die Logik stehen (z.B. ein Programm starten)
        print(f"DOWN: {self}") # Nutzt automatisch __repr__

    def release(self):
        self.state = 0
        print(f"UP:   {self}") # Nutzt automatisch __repr__

# Initialisierung mit den Werten aus der Analyse
def init_keys():
    KEY_MAP.clear()
    
    # Taste 1 bis 7 (Reihe 1 und Anfang Reihe 2) liegen in Byte 42
    # Werte: 2, 4, 8, 16, 32, 64, 128
    for i in range(7):
        bit_val = 2**(i + 1) # Errechnet 2, 4, 8...
        KEY_MAP[i] = DisplaypadKey(index=i+1, byte_pos=42, bit_value=bit_val)
    
    # Taste 8 bis 12 (Rest der Reihe 2) liegen in Byte 47
    # Werte: 1, 2, 4, 8, 16
    for i in range(7, 12):
        bit_val = 2**(i - 7) # Errechnet 1, 2, 4, 8, 16
        KEY_MAP[i] = DisplaypadKey(index=i+1, byte_pos=47, bit_value=bit_val)

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
import hid
import time

# Exakte IDs aus deinem lsusb
VENDOR_ID = 0x3282
DISPLAYPAD_PID = 0x0009 
KEYBOARD_PID = 0x0001

def send_brightness_to_displaypad(level=100):
    """Versucht die Helligkeit des Displaypads zu setzen."""
    try:
        # Wir suchen gezielt das Interface 3 des Displaypads
        target_path = None
        for device in hid.enumerate():
            if device['vendor_id'] == VENDOR_ID and \
               device['product_id'] == DISPLAYPAD_PID and \
               device['interface_number'] == 3:
                target_path = device['path']
                break
        
        if not target_path:
            print("DisplayPad Interface 3 nicht gefunden! Prüfe udev-Rules.")
            return

        h = hid.device()
        h.open_path(target_path)
        
        # Mountain Befehls-Struktur (Vermutung: Report ID 0x02)
        # Byte 0: Report ID (0x02)
        # Byte 1: Command (0x01 = Control?)
        # Byte 2: Sub-Command (0x01 = Brightness?)
        # Byte 3: Value (0-100)
        packet = [0x02, 0x01, 0x01, level] + [0x00] * 60
        
        h.write(packet)
        print(f"Helligkeits-Paket ({level}%) an DisplayPad gesendet!")
        
        h.close()
    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    send_brightness_to_displaypad(50) # Teste mit 50%py
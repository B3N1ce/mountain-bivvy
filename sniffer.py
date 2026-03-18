import hid

# Hex-Werte wie besprochen
VENDOR_ID = 0x3282
PID = 0x0009 # 0x0001 keyboard 0x0009 displaypad

def start_listen():
    try:
        # Wir suchen Interface 0 für die Tasten
        target_path = None
        for device in hid.enumerate(VENDOR_ID, PID):
            if device['interface_number'] == 3:
                target_path = device['path']
                break
        
        if not target_path:
            print("Interface 0 nicht gefunden!")
            return

        h = hid.device()
        h.open_path(target_path)
        print(f"Verbunden mit {target_path.decode()}")
        print("Drücke nacheinander die Tasten am Displaypad...")

        while True:
            # Wir lesen 64 Bytes
            data = h.read(64)
            if data:
                # Wir geben die Daten als Hex-String aus
                print(f"Raw Data: {data}")
                # Meistens ist Byte 0 oder 1 der Key-Index
                
    except KeyboardInterrupt:
        print("\nBeendet.")
    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    start_listen()
    
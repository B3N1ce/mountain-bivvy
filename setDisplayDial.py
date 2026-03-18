import hid

def set_dial_display(value):
    VENDOR_ID = 0x3282
    KEYBOARD_PID = 0x0001
    
    try:
        h = hid.device()
        # Suche Interface 3 des Keyboards
        target_path = next(d['path'] for d in hid.enumerate(VENDOR_ID, KEYBOARD_PID) if d['interface_number'] == 3)
        h.open_path(target_path)
        
        # Das ist ein "Rate-Paket" - wir probieren Command 0x15 (typisch für Dial)
        # Struktur: [ReportID, Command, SubCommand, Value, ...]
        packet = [0x02, 0x15, 0x01, value] + [0x00] * 60
        h.write(packet)
        print(f"Versuche Lautstärke {value} an Display zu senden...")
        h.close()
    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    set_dial_display(50) # Versuche den Balken auf die Mitte zu setzen
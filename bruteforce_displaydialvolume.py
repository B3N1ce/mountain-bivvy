import hid
import time

VENDOR_ID = 0x3282
KEYBOARD_PID = 0x0001 # Everest Max

def brute_force_dial():
    try:
        # Finde Pfad zu Interface 3
        devices = hid.enumerate(VENDOR_ID, KEYBOARD_PID)
        target_path = next((d['path'] for d in devices if d['interface_number'] == 3), None)
        
        if not target_path:
            print("Interface 3 nicht gefunden!")
            return

        h = hid.device()
        h.open_path(target_path)
        print(f"Starte Brute-Force auf {target_path.decode()}...")
        print("Beobachte das Dial-Display!")

        # Wir testen die wahrscheinlichsten Command-Bytes (0x10 bis 0x20)
        # 0x11, 0x15 und 0x16 sind bei Mountain oft für das Dial reserviert.
        for cmd in range(0x10, 0x21):
            for sub_cmd in range(0x00, 0x05):
                test_val = 50 # Wir senden "50%" als Testwert
                
                # Paket-Struktur: [ReportID, Command, Sub-Command, Value, ...]
                packet = [0x02, cmd, sub_cmd, test_val] + [0x00] * 60
                
                print(f"Teste: Report 0x02, Cmd {hex(cmd)}, Sub {hex(sub_cmd)}")
                h.write(packet)
                
                # Kurze Pause, damit die Hardware Zeit zum Verarbeiten hat
                # und du sehen kannst, bei welchem Befehl es reagiert
                time.sleep(0.5) 

        h.close()
        print("Brute-Force abgeschlossen.")

    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    brute_force_dial()
import hid
import time
import subprocess
import re

# Konfiguration
USB_VID = 0x3282
USB_PID = 0x0001
INTERFACE_NUM = 3

def get_system_volume():
    """Liest die aktuelle Lautstärke der Default-Sink via pactl aus."""
    try:
        # Führt pactl aus und sucht nach dem Prozentwert
        output = subprocess.check_output("pactl get-sink-volume @DEFAULT_SINK@", shell=True).decode()
        # Findet die erste Prozentzahl im String (z.B. '50%')
        volume = int(re.search(r'(\d+)%', output).group(1))
        # Cap bei 100, falls Overdrive aktiviert ist
        return min(volume, 100)
    except Exception:
        return 0

def run_sync():
    # Interface 3 suchen
    target_path = None
    for d in hid.enumerate(USB_VID, USB_PID):
        if d['interface_number'] == INTERFACE_NUM:
            target_path = d['path']
            break

    if not target_path:
        print("Fehler: Everest Media Interface nicht gefunden!")
        return

    dev = hid.device()
    dev.open_path(target_path)
    dev.set_nonblocking(True) # Damit read() nicht hängen bleibt

    print("Nobara Dial Sync ist aktiv. Drücke Strg+C zum Beenden.")
    
    last_volume = -1

    try:
        while True:
            current_volume = get_system_volume()

            if current_volume != last_volume:
                # Paket 1: Wakeup
                p1 = [0x00] * 65
                p1[1] = 0x11
                p1[2] = 0x14
                dev.write(p1)
                
                time.sleep(0.005) # 5ms Sicherheitspause
                
                # Paket 2: Daten
                p2 = [0x00] * 65
                p2[1] = 0x11
                p2[2] = 0x83
                p2[5] = current_volume
                dev.write(p2)
                
                # Puffer leeren
                dev.read(64)
                
                last_volume = current_volume
                print(f"Volume-Update: {current_volume}%")

            # Kurze Pause, um die CPU zu schonen (10x pro Sekunde prüfen)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nSync gestoppt.")
    finally:
        dev.close()

if __name__ == "__main__":
    run_sync()
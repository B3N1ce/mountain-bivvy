import os
import socket
import json
import time
import threading
from modules.keyboard.everest_max import EverestMax
from modules.displaypad.displaypad import Displaypad
from utils.audio_provider import AudioProvider

class BivvyDaemon:
    def __init__(self):
        self.socket_path = "/tmp/bivvy.sock"
        self.kb = EverestMax()
        self.dp = Displaypad()
        self.audio = AudioProvider()
        self.running = True
        self.preview_volume = None # Wenn gesetzt, überschreibt dies das System-Audio

    def handle_client(self, conn):
        try:
            data = conn.recv(1024)
            if data:
                msg = json.loads(data.decode())
                cmd = msg.get("command")
                val = msg.get("value")

                if cmd == "SET_VOLUME":
                    self.preview_volume = val
                    if self.kb.dock:
                        self.kb.dock.set_volume(val)
                elif cmd == "RELEASE_CONTROL":
                    self.preview_volume = None
                elif cmd == "RELOAD_CONFIG":
                    self.dp.load_config_and_init_keys()
                    print("Daemon: DisplayPad-Konfiguration aktualisiert.")
        except Exception as e:
            print(f"IPC Error: {e}")
        finally:
            conn.close()

    def displaypad_worker(self):
        """Eigener Thread für die Displaypad-Eingaben."""
        print("Displaypad-Überwachung aktiv...")
        while self.running:
            if self.dp.device:
                try:
                    data = self.dp.device.read(64)
                    if data:
                        self.dp.process_data(data)
                except Exception as e:
                    print(f"Displaypad Read Error: {e}")
                    time.sleep(1) # Kurze Pause bei Fehler
            time.sleep(0.01) # 100Hz Abfrage reicht völlig aus

    def start_ipc_server(self):
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)
            
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(self.socket_path)
        os.chmod(self.socket_path, 0o666)
        server.listen(5)

        def listen_loop():
            while self.running:
                try:
                    conn, _ = server.accept()
                    self.handle_client(conn)
                except Exception:
                    pass

        threading.Thread(target=listen_loop, daemon=True).start()

    def run(self):
        print("Bivvy Daemon startet...")
        if self.kb.connect():
            print("Everest Max verbunden!")
        else:
            print("Everest Max nicht gefunden. Bitte anschließen.")

        if self.dp.connect():
            print("Displaypad verbunden!")
        else:
            print("Displaypad nicht gefunden. Bitte anschließen.")

        # Starte den Displaypad Thread
        threading.Thread(target=self.displaypad_worker, daemon=True).start()

        self.start_ipc_server()
        last_vol = -1

        try:
            while self.running:
                # Normaler Audio-Sync läuft nur, wenn die GUI nicht gerade testet
                if self.preview_volume is None:
                    current_vol = self.audio.get_volume()
                    if current_vol != last_vol and self.kb.dock:
                        self.kb.dock.set_volume(current_vol)
                        last_vol = current_vol
                else:
                    # Damit bei Release Control sofort wieder gesynct wird
                    last_vol = -1 
                
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nBeende Bivvy Daemon...")
        finally:
            self.running = False
            self.kb.disconnect()
            if os.path.exists(self.socket_path):
                os.remove(self.socket_path)

if __name__ == "__main__":
    daemon = BivvyDaemon()
    daemon.run()
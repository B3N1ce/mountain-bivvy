import sys
import subprocess
import time

def start_gui():
    print("Starte Bivvy Control Center...")
    # Wir nutzen sys.executable, um sicherzustellen, dass das gleiche 
    # Python-Environment (Venv) genutzt wird.
    subprocess.Popen([sys.executable, "-m", "gui.main_window"])

if __name__ == "__main__":
    # Hier könntest du später prüfen, ob der Daemon läuft
    # und ihn ggf. mit starten.
    start_gui()
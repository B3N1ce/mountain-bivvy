import sys
import subprocess
import time
import os
import socket

def is_daemon_running(socket_path="/tmp/bivvy.sock"):
    """Prüft, ob der Daemon läuft, indem versucht wird, den Socket zu erreichen."""
    if not os.path.exists(socket_path):
        return False
    try:
        # Versuche eine Verbindung zum Socket aufzubauen
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(socket_path)
        client.close()
        return True
    except (socket.error, ConnectionRefusedError):
        return False

def start_daemon():
    print("Daemon nicht gefunden. Starte Bivvy Daemon...")
    # Popen wird hier bewusst genutzt, damit der Daemon im Hintergrund bleibt
    subprocess.Popen([sys.executable, "bivvy_daemon.py"], 
                     stdout=subprocess.DEVNULL, 
                     stderr=subprocess.DEVNULL)
    # Kurz warten, damit der Daemon den Socket erstellen kann
    time.sleep(1.5)

def start_gui():
    print("Starte Bivvy Control Center...")
    # .run() statt .Popen() blockiert das Skript, bis die GUI geschlossen wird
    try:
        subprocess.run([sys.executable, "-m", "gui.main_window"], check=True)
    except KeyboardInterrupt:
        pass
    print("GUI wurde geschlossen. Beende Hauptskript.")

if __name__ == "__main__":
    # 1. Check den Daemon via Socket
    if not is_daemon_running():
        start_daemon()
    else:
        print("Bivvy Daemon läuft bereits.")

    # 2. Starte die GUI (blockierend)
    start_gui()
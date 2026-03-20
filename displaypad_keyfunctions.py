import subprocess

# --- KATEGORIE: SYSTEM-STEUERUNG ---

def toggle_mute():
    print("ACTION: Audio stummschalten/aktivieren")
    subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "toggle"])

def volume_up():
    print("ACTION: Lautstärke +5%")
    subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+5%"])

def volume_down():
    print("ACTION: Lautstärke -5%")
    subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-5%"])

def system_suspend():
    print("ACTION: PC in den Energiesparmodus versetzen")
    subprocess.run(["systemctl", "suspend"])

# --- KATEGORIE: MEDIA-PLAYER (Spotify, YouTube, VLC) ---

def media_play_pause():
    print("ACTION: Media Play/Pause")
    subprocess.run(["playerctl", "play-pause"])

def media_next():
    print("ACTION: Nächster Titel")
    subprocess.run(["playerctl", "next"])

def media_prev():
    print("ACTION: Vorheriger Titel")
    subprocess.run(["playerctl", "previous"])

# --- KATEGORIE: ANWENDUNGEN STARTEN ---

def start_terminal():
    print("ACTION: Terminal öffnen")
    # Nobara nutzt oft gnome-terminal oder kgx
    subprocess.Popen(["gnome-terminal"])

def open_default_browser():
    print("ACTION: Standardbrowser öffnen")
    # 'gtk-launch' startet die verknüpfte .desktop Datei
    # 'xdg-settings' enthält den Standardbrowser
    try:
        # Standard-Browser-Handler ermitteln"
        cmd = "xdg-settings get default-web-browser"
        browser_desktop_file = subprocess.check_output(cmd.split()).decode().strip()
        # browser_desktop_file ist meistens etwas wie "firefox.desktop"
        
        # Jetzt starten wir genau diese Desktop-Datei
        subprocess.Popen(["gtk-launch", browser_desktop_file])
    except Exception as e:
        print(f"FEHLER beim Finden des Standardbrowsers: {e}")
        # Fallback: Falls alles schiefgeht, versuche einfach 'firefox'
        subprocess.Popen(["firefox"])

def start_calculator():
    print("ACTION: Taschenrechner öffnen")
    subprocess.Popen(["gnome-calculator"])

def open_file_manager():
    print("ACTION: Dateimanager öffnen")
    subprocess.Popen(["nautilus", os.path.expanduser("~")])

def start_app(app_name: str):
    print(f"ACTION: Starte Anwendung: {app_name}")
    try:
        subprocess.Popen([app_name])
    except FileNotFoundError:
        print(f"FEHLER: Anwendung '{app_name}' wurde nicht gefunden.")

# --- KATEGORIE: TOOLS & SCREENSHOTS ---

def take_screenshot():
    print("ACTION: Screenshot vom Bereich erstellen")
    # Nutzt das GNOME-Screenshot Tool
    subprocess.Popen(["gnome-screenshot", "-a"])

def toggle_night_light():
    print("ACTION: Nachtmodus (Blaulichtfilter) umschalten")
    # Dies ist ein Beispiel für ein gsettings-Kommando (GNOME)
    cmd = "gsettings get org.gnome.settings-daemon.plugins.color night-light-enabled"
    current = subprocess.check_output(cmd.split()).decode().strip()
    new_state = "false" if current == "true" else "true"
    subprocess.run(["gsettings", "set", "org.gnome.settings-daemon.plugins.color", "night-light-enabled", new_state])

# --- KATEGORIE: ENTWICKLUNG / DEBUG ---

def print_hello():
    print("ACTION: Hello World Test-Ausgabe")

def show_system_resources():
    print("ACTION: Systemmonitor (btop/htop) im neuen Terminal")
    subprocess.Popen(["gnome-terminal", "--", "btop"])

def printText(text:str):
    print("ACTION: Print Text = {text}")
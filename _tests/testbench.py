import sys
import os
import json
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Pfad für die temporären Fensterdaten
GEOMETRY_FILE = ".window_geometry.json"

def save_geometry(window):
    """Speichert Position und Größe des Fensters."""
    if window:
        geometry = {
            "x": window.property("x"),
            "y": window.property("y"),
            "width": window.property("width"),
            "height": window.property("height")
        }
        with open(GEOMETRY_FILE, "w") as f:
            json.dump(geometry, f)

def load_geometry():
    """Lädt die letzte Position und Größe."""
    if os.path.exists(GEOMETRY_FILE):
        try:
            with open(GEOMETRY_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return None

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, engine, app):
        self.engine = engine
        self.app = app

    def on_modified(self, event):
        if event.src_path.endswith(".qml") or event.src_path.endswith("qmldir"):
            # Hol dir das Hauptfenster aus der Engine
            root_objects = self.engine.rootObjects()
            if root_objects:
                save_geometry(root_objects[0])
            
            print(f"🔄 Reloading and restoring position...")
            os.execl(sys.executable, sys.executable, *sys.argv)

if __name__ == "__main__":
    # Zwinge Qt dazu, XWayland zu nutzen, damit x/y gesetzt werden dürfen
    os.environ["QT_QPA_PLATFORM"] = "xcb"

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    qml_path = os.path.join(os.path.dirname(__file__), "gui/testbench.qml")
    engine.load(qml_path)

    # Fenster-Position wiederherstellen
    root_objects = engine.rootObjects()
    if root_objects:
        window = root_objects[0]
        geo = load_geometry()
        if geo:
            window.setProperty("x", geo["x"])
            window.setProperty("y", geo["y"])
            window.setProperty("width", geo["width"])
            window.setProperty("height", geo["height"])

    # Watcher Setup
    observer = Observer()
    handler = ReloadHandler(engine, app)
    observer.schedule(handler, path=os.path.dirname(__file__), recursive=True)
    observer.start()

    sys.exit(app.exec())
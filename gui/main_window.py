import sys
import os
import socket
import json
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QSlider, QFrame, QTabWidget, 
                             QGridLayout, QComboBox, QMessageBox, QDialog, QDialogButtonBox)
from PySide6.QtCore import Qt

# Import des Pfad-Fixes und der Funktionen
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.append(root_path)

from modules.displaypad.displaypad_keyfunctions import AVAILABLE_ACTIONS

class BivvyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bivvy Control Center")
        self.setMinimumSize(700, 450)
        self.socket_path = "/tmp/bivvy.sock"
        self.config_path = os.path.join(root_path, "config.json")
        
        # 1. Erst die bestehende Konfiguration laden
        self.displaypad_assignments = self.load_existing_config()
        
        # 2. Dann das UI aufbauen (nutzt jetzt die geladenen Daten)
        self.init_ui()

    def load_existing_config(self):
        """Liest die config.json aus und gibt ein Mapping für die 12 Tasten zurück."""
        assignments = {i: "Nicht belegt" for i in range(1, 13)}
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                    key_data = config.get("keys", {})
                    for key_str, data in key_data.items():
                        idx = int(key_str)
                        action_name = data.get("action", "Nicht belegt")
                        if idx in assignments:
                            assignments[idx] = action_name
                print("Konfiguration erfolgreich geladen.")
            except Exception as e:
                print(f"Fehler beim Laden der config.json: {e}")
        
        return assignments

    def init_ui(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Tabs erstellen
        self.tab_everest = QWidget()
        self.tab_mediadial = QWidget()
        self.tab_numpad = QWidget()
        self.tab_displaypad = QWidget()

        self.tabs.addTab(self.tab_everest, "Everest Max")
        self.tabs.addTab(self.tab_mediadial, "Media Dock")
        self.tabs.addTab(self.tab_numpad, "Numpad")
        self.tabs.addTab(self.tab_displaypad, "DisplayPad")


        self.build_everest_tab()
        self.build_mediadial_tab()
        self.build_numpad_tab()
        self.build_displaypad_tab()

        self.setCentralWidget(central_widget)

# --- TAB 1: EVEREST MAX ---
    def build_everest_tab(self):
        layout = QVBoxLayout(self.tab_everest)
        label = QLabel("Haupteinstellungen der Tastatur (z.B. Polling Rate, Global RGB)")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

    # --- TAB 2: MEDIA DOCK ---
    def build_mediadial_tab(self):
        layout = QVBoxLayout(self.tab_mediadial)

        title = QLabel("Media Dock - Lautstärke Vorschau")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.valueChanged.connect(self.on_slider_move)
        layout.addWidget(self.slider)

        self.vol_display = QLabel("Bewege den Slider zum Testen")
        self.vol_display.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.vol_display)

        self.btn_release = QPushButton("System-Audio Sync fortsetzen")
        self.btn_release.clicked.connect(self.release_control)
        layout.addWidget(self.btn_release)
        layout.addStretch() # Drückt alles nach oben

    # --- TAB 3: NUMPAD ---
    def build_numpad_tab(self):
        layout = QVBoxLayout(self.tab_numpad)
        label = QLabel("Numpad Einstellungen (Zukünftige Funktionen)")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

    # --- TAB 4: DISPLAYPAD ---
    def build_displaypad_tab(self):
        layout = QVBoxLayout(self.tab_displaypad)
        
        info = QLabel("DisplayPad Tastenbelegung (Klicke auf eine Taste, um sie zu ändern)")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)

        # Ein Grid-Layout für die 2x6 Tasten
        grid = QGridLayout()
        grid.setSpacing(10)
        
        self.dp_buttons = {}
        
        # Erstelle 12 Buttons (2 Reihen, 6 Spalten)
        for row in range(2):
            for col in range(6):
                key_index = row * 6 + col + 1
                
                # Button, der wie eine DisplayPad-Taste aussieht
                btn = QPushButton()
                btn.setFixedSize(80, 80)
                
                # Zeilenumbrüche für bessere Lesbarkeit
                current_func = self.displaypad_assignments[key_index]
                btn.setText(f"Taste {key_index}\n\n{current_func}")
                
                # Klick-Event mit dem key_index verknüpfen (Lambda closure)
                btn.clicked.connect(lambda checked, k=key_index: self.on_displaypad_key_clicked(k))
                
                grid.addWidget(btn, row, col)
                self.dp_buttons[key_index] = btn

        # Grid zentrieren
        grid_container = QWidget()
        grid_container.setLayout(grid)
        layout.addWidget(grid_container, alignment=Qt.AlignCenter)
        layout.addStretch()

    def on_displaypad_key_clicked(self, key_index):
        # 1. Dialog öffnen und Funktion wählen
        current = self.displaypad_assignments.get(key_index)
        dialog = ActionSelectDialog(self.displaypad_assignments.get(key_index), self)
        
        if dialog.exec():
            new_action = dialog.get_selected_action()
            
            # 1. GUI Update
            self.displaypad_assignments[key_index] = new_action
            self.dp_buttons[key_index].setText(f"Taste {key_index}\n\n{new_action}")
            
            # 2. Speichern & Daemon benachrichtigen
            self.save_and_reload(key_index, new_action)

    def save_and_reload(self, key_index, action_name):
        # Config laden oder neu erstellen
        config = {"keys": {}}
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                config = json.load(f)

        # Update
        config["keys"][str(key_index)] = {"action": action_name}

        # Speichern
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=4)

        # Daemon Signal
        self.send_command("RELOAD_CONFIG")

    def on_slider_move(self, value):
        self.vol_display.setText(f"Vorschau: {value} %")
        self.send_command("SET_VOLUME", value)

    def release_control(self):
        self.vol_display.setText("System-Audio Sync aktiv")
        self.slider.setValue(0)
        self.send_command("RELEASE_CONTROL")

    def send_command(self, cmd, val=None):
        try:
            client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            client.connect(self.socket_path)
            msg = json.dumps({"command": cmd, "value": val})
            client.send(msg.encode())
            client.close()
        except FileNotFoundError:
            pass # Ignorieren wir im Prototyp, wenn Daemon aus ist
        except Exception as e:
            print(f"Fehler beim Senden: {e}")

    def save_assignment(self, key_index, action_name):
        config_path = "config.json"
        
        # 1. Bestehende Config laden
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)
        else:
            config = {"keys": {}}

        # 2. Wert aktualisieren
        config["keys"][str(key_index)] = {"action": action_name}

        # 3. Speichern
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)

        # 4. Dem Daemon sagen: "Lade die Config neu!"
        self.send_command("RELOAD_CONFIG")

class ActionSelectDialog(QDialog):
    def __init__(self, current_action, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Aktion auswählen")
        layout = QVBoxLayout(self)

        self.combo = QComboBox()
        self.combo.addItems(list(AVAILABLE_ACTIONS.keys()))
        if current_action in AVAILABLE_ACTIONS:
            self.combo.setCurrentText(current_action)
        
        layout.addWidget(QLabel("Wähle eine Funktion für diese Taste:"))
        layout.addWidget(self.combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_selected_action(self):
        return self.combo.currentText()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BivvyGUI()
    window.show()
    sys.exit(app.exec())
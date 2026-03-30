import sys
import os
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterSingletonType
from PySide6.QtCore import QTimer, QObject, Property, Signal

class Bridge(QObject):
    temp_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self._temp = 42
        # Simuliere CPU-Temperaturänderung alle 2 Sekunden
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_temp)
        self.timer.start(2000)

    def update_temp(self):
        self._temp = (self._temp + 1) % 100
        self.temp_changed.emit(self._temp)

    @Property(int, notify=temp_changed)
    def cpu_temp(self):
        return self._temp

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Registriere die Bridge, damit QML darauf zugreifen kann
    bridge = Bridge()
    engine.rootContext().setContextProperty("python", bridge)

    # Lade die Hauptdatei
    qml_file = os.path.join(os.path.dirname(__file__), "Main.qml")
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
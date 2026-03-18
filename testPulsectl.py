import pulsectl

def get_current_volume():
    with pulsectl.Pulse('volume-checker') as pulse:
        # Hole die Standard-Ausgabe (Sink)
        sink = pulse.sink_list()[0] 
        # Lautstärke ist ein Durchschnittswert aller Kanäle (L/R)
        volume = round(sink.volume.value_flat * 100)
        print(f"System-Lautstärke: {volume}%")
        return volume

if __name__ == "__main__":
    get_current_volume()
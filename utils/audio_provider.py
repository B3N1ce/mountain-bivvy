import subprocess
import re

class AudioProvider:
    def get_volume(self):
        try:
            output = subprocess.check_output("pactl get-sink-volume @DEFAULT_SINK@", shell=True).decode()
            match = re.search(r'(\d+)%', output)
            return min(int(match.group(1)), 100) if match else 0
        except Exception:
            return 0
import os
import hid

#TODO: make it work, unbind not happening (path not found?)

def silence_displaypad_keyboard():
    vendor_id = 0x3282
    product_id = 0x0009
    
    # Wir suchen Interface 1 (das Keyboard-Interface)
    itfs = hid.enumerate(vendor_id, product_id)
    target_path = None
    
    for d in itfs:
        if d['interface_number'] == 1:
            # Der Pfad von hidapi sieht oft so aus: 0005:000b:01
            # Wir brauchen aber den Kernel-Pfad (z.B. 5-4.3:1.1)
            # Ein einfacher Trick unter Linux ist die Nutzung von 'sysfs'
            raw_path = d['path'].decode('utf-8')
            # Extrahiere den USB-Bezeichner aus dem Pfad (distro-abhängig)
            # Oft hilft ein Blick in /sys/class/hidraw/hidrawX/device
            print(f"Versuche Interface 1 zu finden: {raw_path}")

    # Für den Moment ist der manuelle Weg über den Pfad, den du kennst, sicherer:
    kernel_dev = "5-4.3:1.1" 
    unbind_path = f"/sys/bus/usb/drivers/usbhid/unbind"
    
    if os.path.exists(f"/sys/bus/usb/drivers/usbhid/{kernel_dev}"):
        print(f"Deaktiviere störendes HID-Binding für {kernel_dev}...")
        os.system(f'echo "{kernel_dev}" | sudo tee {unbind_path} > /dev/null')

if __name__ == "__main__":
    silence_displaypad_keyboard()
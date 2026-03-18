import hid

def scan_mountain_devices():
    print(f"{'Path':<40} | {'IF':<3} | {'Usage Page':<6} | {'Product'}")
    print("-" * 80)
    for device in hid.enumerate():
        # Mountain Vendor ID ist 0x3282
        if device['vendor_id'] == 0x3282:
            path = device['path'].decode('utf-8')
            if_num = device['interface_number']
            usage_pg = device['usage_page']
            product = device['product_string']
            print(f"{path:<40} | {if_num:<3} | {usage_pg:<10} | {product}")

if __name__ == "__main__":
    scan_mountain_devices()
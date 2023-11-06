# Sure! Here's a script that uses the Scapy library in Python to capture handshake packets from a specific MAC address of a WiFi network:

# python in turmex android
#!/usr/bin/env python3

from scapy.all import Dot11, Dot11Beacon, Dot11Elt, Dot11ProbeResp, RadioTap, srp, rdpcap

# Put the MAC address of the target WiFi network here
target_mac = "xx:xx:xx:xx:xx:xx"

def get_handshake_packets(packets):
    """Filter packets to find handshake packets"""
    wpa_handshake_messages = (0x00, 0x01, 0x02, 0x03)

    handshake_packets = []
    for packet in packets:
        if packet.haslayer(Dot11) and packet.type == 2:
            if packet.subtype == 0x08:
                # Beacon frame
                if packet.haslayer(Dot11Beacon):
                    if packet.addr2 == target_mac:
                        handshake_packets.append(packet)
            elif packet.subtype == 0x05:
                # Probe response frame
                if packet.haslayer(Dot11ProbeResp):
                    if packet.addr2 == target_mac:
                        handshake_packets.append(packet)
            elif packet.subtype == 0x0b:
                # Data frame
                if packet.haslayer(Dot11Elt):
                    if packet.addr2 == target_mac and packet.info.startswith(b"WPA"):
                        handshake_packets.append(packet)
            elif packet.subtype in wpa_handshake_messages:
                # EAPOL packets (handshake messages)
                handshake_packets.append(packet)

    return handshake_packets

def capture_handshake(target_mac):
    """Capture handshake packets from the target MAC address"""
    print("Sniffing WiFi packets, press Ctrl+C to stop...")
    packets = rdpcap("wifi.pcap")
    handshake_packets = get_handshake_packets(packets)

    if handshake_packets:
        print(f"Found {len(handshake_packets)} handshake packets:")
        for packet in handshake_packets:
            print(packet.summary())
    else:
        print("No handshake packets found.")

if __name__ == "__main__":
    capture_handshake(target_mac)


# Before running the script, make sure to install the required dependencies by executing `pip install scapy` in your Termux environment. Make sure to replace `"xx:xx:xx:xx:xx:xx"` in the `target_mac` variable with the MAC address of the WiFi network you want to capture the handshake from.

# To run the script, save it to a file (e.g., `wifi_capture.py`) and execute `python3 wifi_capture.py` in your Termux environment. The script will read packets from a file named `wifi.pcap` (change the filename as needed) and filter out any handshake packets from the specified MAC address. The captured handshake packets (if any) will be displayed on the console.

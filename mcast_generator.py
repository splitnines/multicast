import argparse
import datetime as dt
import socket
import random
import string
import struct
import sys
import time


# Parse cli arguments
def cli_args():
    parser = argparse.ArgumentParser(
        description="A multicast server/client data generator."
    )
    parser.add_argument(
        "-c",
        "--client",
        action="store_true",
        help="Run as a multicast client/receiver.",
    )
    parser.add_argument(
        "-s",
        "--server",
        action="store_true",
        help="Run as a multicast server/sender.",
    )
    parser.add_argument(
        "-r",
        "--rate",
        type=int,
        default=1,
        help="(Optional): the rate in packets/sec to send IGMP messages "
        "(default 1 packet/sec)",
    )
    parser.add_argument(
        "-g",
        "--group",
        type=str,
        default="239.255.255.1",
        help="(Optional): the multicast group address to join/leave "
        "(default 239.255.255.1)",
    )
    parser.add_argument(
        "-t",
        "--time",
        type=int,
        default=0,
        help="(Optional): the amount of time to run the spammer "
        "(default continious)",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=12345,
        help="(Optional): which port to listen/send on (default port 12345)",
    )
    parser.add_argument(
        "-i",
        "--interface",
        type=str,
        default=None,
        help="(Optional): specify an interface to listen/send on",
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()


def generate_random_data(length=1024):
    random_data = (
        string.ascii_letters + string.digits + string.punctuation + " "
    )
    return "".join(random.choice(random_data) for _ in range(length))


def mcast_server(group, port, rate, duration, iface):
    server = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
    )

    ttl = struct.pack("b", 32)
    server.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    if iface is not None:
        server.setsockopt(
            socket.SOL_SOCKET, socket.SO_BINDTODEVICE, iface.encode()
        )

    random_data = generate_random_data()
    packet_num = 1

    start_time = time.time()

    try:
        while True:
            if duration > 0 and (time.time() - start_time >= duration):
                break

            print(
                f"{packet_num} {dt.datetime.now()} sending "
                f"{len(random_data)} bytes to {group}({port})"
            )
            server.sendto(random_data.encode("utf8"), (group, port))
            packet_num += 1
            time.sleep(1 / rate)

    except KeyboardInterrupt:
        print("\n\nMulticast generator stopped.\n")
    finally:
        server.close()


def mcast_client(group, port, iface):
    client = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
    )
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if iface is not None:
        client.setsockopt(
            socket.SOL_SOCKET, socket.SO_BINDTODEVICE, iface.encode()
        )

    client.bind(("", port))

    igmp_req = struct.pack("4sl", socket.inet_aton(group), socket.INADDR_ANY)
    client.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, igmp_req)

    print(f"\n\nListening for multicast stream on {group}({port})...\n")

    packet_num = 1
    try:
        while True:
            data, address = client.recvfrom(1024)
            print(
                f"{packet_num} {dt.datetime.now()} received "
                f"{len(data)} bytes from {address[0]}"
            )
            packet_num += 1

    except KeyboardInterrupt:
        print("\n\nMulticast client stopped.\n")
    finally:
        client.setsockopt(
            socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, igmp_req
        )
        client.close()


def main():
    args = cli_args()
    rate_pps = args.rate
    mcast_group = args.group
    mcast_port = args.port
    duration = args.time
    iface = args.interface

    if args.server is True:
        mcast_server(mcast_group, mcast_port, rate_pps, duration, iface)
    if args.client is True:
        mcast_client(mcast_group, mcast_port, iface)


if __name__ == "__main__":
    main()

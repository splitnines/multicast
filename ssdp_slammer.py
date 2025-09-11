import datetime as dt
import socket
import time

GROUP = "239.255.255.250"
PORT = 1900

SSDP_MESSAGE = (
    "M-SEARCH * HTTP/1.1\r\n"
    f"HOST: {GROUP}:{PORT}\r\n"
    "MAN: \"ssdp:discover\"\r\n"
    "MX: 3\r\n"
    "ST: ssdp:all\r\n"
    "\r\n"
).encode("utf-8")


def send_ssdp_flood(rate=100, duration=10):
    print(
        f"Sending SSDP multicast flood to {GROUP}:{PORT} "
        f"at {rate} packets/sec for {duration} seconds.")

    sock = socket.socket(
        socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
    )

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    packet_num = 1
    start_time = time.time()
    try:
        while True:
            if duration > 0 and (time.time() - start_time >= duration):
                break

            print(f"{packet_num} {dt.datetime.now()} "
                  f"sending SSDP packet {GROUP} {PORT}")
            sock.sendto(SSDP_MESSAGE, (GROUP, PORT))
            packet_num += 1
            time.sleep(1 / rate)  # Control the rate
    except KeyboardInterrupt:
        print("\n\nSSDP Slammer stopped\n")
    finally:
        sock.close()


if __name__ == "__main__":
    send_ssdp_flood(rate=200, duration=0)

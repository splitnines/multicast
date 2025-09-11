import argparse
import datetime as dt
import socket
import struct
import time


# Parse cli arguments
def cli_args():
    parser = argparse.ArgumentParser(
        description="Spams IGMP Joim/Leave messages on an interface"
    )
    parser.add_argument(
        "-r", "--rate", type=float, default=1.0,
        help="The rate in packets/sec to send IGMP messages (default 1 packet/sec)"
    )
    parser.add_argument(
        "-g", "--group", type=str, default="239.255.255.1",
        help="The multicast group address to join/leave (default 239.255.255.1)"
    )
    parser.add_argument(
        "-t", "--time", type=int, default=0,
        help="The amount of time to run the spammer (default continious)"
    )
    parser.add_argument(
        "-j", "--join_only", action="store_true",
        help="Only send IGMP Join messages"
    )

    return parser.parse_args()



# IGMP sp-sp-sp-spammer
def igmp_spam(rate, group, duration, **kwargs):

    try :
        packet_num = 1
        start_time = time.time()

        while True:

            if duration > 0 and (time.time() - start_time >= duration):
                break

            igmp_spammer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            igmp_spammer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	           
            igmp_spammer.bind(('', 12345))
	           
            igmp_msg = struct.pack("4sl", socket.inet_aton(group), socket.INADDR_ANY)

            igmp_spammer.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, igmp_msg)
            print(f"{packet_num} {dt.datetime.now()} JOIN multicast group {group}")
            packet_num += 1
            time.sleep(1 / rate)
    
            if kwargs['join_only'] is False:
                igmp_spammer.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, igmp_msg)
                print(f"{packet_num} {dt.datetime.now()} LEAVE multicast group {group}")
                packet_num += 1
                time.sleep(1 / rate)
	        
            igmp_spammer.close()

    except KeyboardInterrupt:
        print("\n\nIGMP Spammer Terminated.\n")
        igmp_spammer.close()
    except Exception:
        print("\n\nCaught general exception.\n")
    finally:
        igmp_spammer.close()



def main():
    args = cli_args()
    rate_pps = args.rate
    mcast_group = args.group
    duration = args.time
    join_only = args.join_only

    igmp_spam(rate_pps, mcast_group, duration, join_only=join_only)


if __name__ == "__main__":
	main()

# Multicast Tools

A collection of multicast‑testing utilities for lab environments and network recreate scenarios.

## Overview

This repository contains a set of Python‑based tools designed to generate, manipulate, and test IP multicast traffic in lab / network recreation scenarios. These tools are useful for validating multicast forwarding, IGMP/MLD group behaviour, flooding quirks, and other multicast‑specific network conditions.

## Included Tools

* `igmp_spammer.py` – generates IGMP join/leave traffic to stress test IGMP behaviour.
* `mcast_generator.py` – creates multicast UDP traffic on specified group(s) and port(s).
* `ssdp_slammer.py` – floods SSDP (multicast) messages for testing device discovery and flooding behaviour.
* `tcn_flood.py` – generates topology change notifications (TCNs) for spurious STP / topology‑reconfiguration scenarios (where applicable).

> Note: As this is a lab and recreate toolset, please use responsibly and **only** in isolated test/lab networks—these tools may disrupt production environments.

## Getting Started

### Requirements

* Python 3 (recommended)
* Appropriate permissions / network privileges to send/receive multicast traffic on the test network
* Hosts/interfaces correctly configured to allow multicast (IGMP/MLD, PIM, etc) or intentionally mis‑configured for recreate testing

### Installation

```bash
git clone https://github.com/splitnines/multicast.git  
cd multicast  
# (optional) create virtual environment  
python3 -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  # if any dependencies  
```

### Usage Examples

#### `mcast_generator.py`

```bash
python3 mcast_generator.py --group 239.1.1.1 --port 5000 --ttl 10 --interval 500  
```

Send UDP packets continuously to multicast group `239.1.1.1:5000` with TTL 10 and 500ms between packets.

#### `igmp_spammer.py`

```bash
python3 igmp_spammer.py --group 224.0.0.5 --count 1000 --leave-after 30  
```

Generate 1000 IGMP join/leave cycles for group `224.0.0.5`, leaving after 30 seconds.

#### `ssdp_slammer.py`

```bash
python3 ssdp_slammer.py --target-device "MyDevice" --repeat 100  
```

Flood SSDP traffic for device discovery tests.

#### `tcn_flood.py`

```bash
python3 tcn_flood.py --vlan 100 --repeat 50  
```

Simulate topology‑change notifications for VLAN 100 fifty times.

## Use Cases & Scenarios

* Validate that a network switch/router correctly handles IGMP joins/leaves, and only forwards multicast traffic to group members (i.e., IGMP snooping behaviour).
* Stress‑test multicast forwarding paths by generating high volume or erratic multicast UDP traffic (via `mcast_generator.py`).
* Recreate multicast misconfigurations (flooding, missing IGMP membership reports, unintended traffic flooding) for lab‑based learning.
* Test device discovery behaviours (via SSDP flooding) and topology‑change effects in multicast‑heavy networks.

## Warnings & Best Practices

* **Always** use in a confined lab or test environment. These tools can generate traffic patterns that may bring down mis‑configured or production networks.
* Ensure TTL values, interface binding, and multicast group address ranges are chosen carefully. Improper use may cause cross‑layer flooding or unintended network impact.
* Monitor network equipment resources during tests—multicast traffic duplication and tree building can place load on switches/routers.
* Be aware of IGMP and MLD configurations on your test network; if snooping or proxying aren’t enabled, behaviour may differ.

## Contributing

Contributions are welcome! If you have enhancements, new tools, bug‑fixes, or scenario scripts, please submit a pull request.
Before submitting, please ensure:

* your code follows the existing style
* you document any new command‑line options or behaviour
* you include tests or example scenarios if applicable

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgements / References

* For background on multicast and group management, see “IGMP Snooping: A Comprehensive Network Multicast Guide”.
* Useful prior‑art on multicast traffic generation and testing includes the NASA/NRL MGEN tool.

---

> *“A collection of multicast tools I use for lab testing and recreates.”*
> — splitnines, multicast repository


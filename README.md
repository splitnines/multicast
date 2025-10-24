# Multicast Tools

A collection of multicast‑testing utilities for lab environments and network recreate scenarios.

## Overview

This repository contains a set of Python‑based tools designed to generate, manipulate, and test IP multicast traffic in lab / network recreation scenarios. These tools are useful for validating multicast forwarding, IGMP group behaviour, flooding quirks, and other multicast‑specific network conditions.

## Included Tools

* `igmp_spammer.py` – generates IGMP join/leave traffic to stress test IGMP behaviour.
* `mcast_generator.py` – creates multicast UDP traffic on specified group(s) and port(s).
* `ssdp_slammer.py` – floods SSDP (multicast) messages for testing device discovery and flooding behaviour.
* `tcn_flood.py` – generates topology change notifications (TCNs) for spurious STP / topology‑reconfiguration scenarios (where applicable).

> Note: As this is a lab and recreate toolset, please use responsibly and **only** in isolated test/lab networks—these tools may disrupt production environments.

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
---

> *“A collection of multicast tools I use for lab testing and recreates.”*
> — splitnines, multicast repository


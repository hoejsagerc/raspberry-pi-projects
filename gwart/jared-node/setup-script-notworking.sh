#!/bin/bash

sudo apt update && sudo apt upgrade -y

sudo apt install git build-essential dkms raspberrypi-kernel-headers -y

git clone https://github.com/cilynx/rtl88x2bu
cd rtl88x2bu/

sed -i 's/I386_PC = y/I386_PC = n/' Makefile
# Remember, change this if you're using a 64-bit kernel
sed -i 's/ARM_RPI = n/ARM_RPI = y/' Makefile

VER=$(sed -n 's/\PACKAGE_VERSION="\(.*\)"/\1/p' dkms.conf)
sudo rsync -rvhP ./ /usr/src/rtl88x2bu-${VER}
sudo dkms add -m rtl88x2bu -v ${VER}
sudo dkms build -m rtl88x2bu -v ${VER} # Takes ~3-minutes on a 3B+
sudo dkms install -m rtl88x2bu -v ${VER}
sudo modprobe 88x2bu

sudo apt update

sudo apt install hostapd dnsmasq -y

sudo DEBIAN_FRONTEND=noninteractive apt install -y netfilter-persistent iptables-persistent

sudo systemctl unmask hostapd.service

sudo systemctl enable hostapd.service

sudo cat > /etc/dhcpcd.conf << EOF
interface wlan1
    static ip_address=10.0.0.1/24
    nohook wpa_supplicant
EOF

sudo cat > /etc/systcl.d/routed-ap.conf << EOF
net.ipv4.ip_forward=1
EOF

sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE

sudo netfilter-persistent save

sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.bk

sudo touch /etc/dnsmasq.conf

sudo cat > /etc/dnsmasq.conf << EOF
interface=wlan1
dhcp-range=10.0.0.200,10.0.0.250,255.255.255.0,72h
domain=wlan
address=/rt.wlan/10.0.0.1
EOF

sudo touch /etc/hostapd/hostapd.conf

sudo cat > /etc/hostapd/hostapd.conf << EOF
interface=wlan1
ssid=gwart-net
hw_mode=a
channel=36
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=P@55w0rd
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
EOF
# gwart
Raspberry Pi Super Computer Cluster


## Configuring the Control Node

### Setting a Password if you configured SSH with key file

```bash
sudo passwd pi

"password"...
"password"...
```

### Installing the wlan nic drivers for tp-link archer AC1300 Archer T3U plus

not used --> Github page: https://github.com/fastoe/RTL8812BU_for_Raspbian

https://raspberrypi.stackexchange.com/questions/100682/second-wifi-adapter-for-the-raspberry-pi-4-b


```bash
# Update all packages per normal
sudo apt update
sudo apt upgrade

# Install prereqs
# Remove raspberrypi-kernel-headers if you're running Ubuntu or you get package-not-found errors
sudo apt install git build-essential dkms raspberrypi-kernel-headers -y

# Reboot just in case there were any kernel updates, you can skip if there weren't
sudo reboot

# Pull down the driver source
git clone https://github.com/cilynx/rtl88x2bu
cd rtl88x2bu/

# Configure for RasPi
sed -i 's/I386_PC = y/I386_PC = n/' Makefile
# Remember, change this if you're using a 64-bit kernel
sed -i 's/ARM_RPI = n/ARM_RPI = y/' Makefile

VER=$(sed -n 's/\PACKAGE_VERSION="\(.*\)"/\1/p' dkms.conf)
sudo rsync -rvhP ./ /usr/src/rtl88x2bu-${VER}
sudo dkms add -m rtl88x2bu -v ${VER}
sudo dkms build -m rtl88x2bu -v ${VER} # Takes ~3-minutes on a 3B+
sudo dkms install -m rtl88x2bu -v ${VER}
sudo modprobe 88x2bu
```

then when if you run:

```bash
ip addr
```

and you should see the new wlan1 nice

```plaintext
4: wlan1: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN group default qlen 1000
    link/ether 60:a4:b7:54:f3:0a brd ff:ff:ff:ff:ff:ff
```

### Installing packages for Router config

```bash
sudo apt update

sudo apt install hostapd dnsmasq -y

sudo DEBIAN_FRONTEND=noninteractive apt install -y netfilter-persistent iptables-persistent
```

### Configuring the Raspberry Pi as a Router

```bash
sudo systemctl unmask hostapd.service

sudo systemctl enable hostapd.service
```

configuring the dhcp configurations

```bash
sudo vim /etc/dhcpcd.conf
```

then go to the bottom and enter the following:

```bash
interface wlan1
    static ip_address=10.1.1.1/24
    nohook wpa_supplicant
```

then for routing from wlan0(wan port) to wlan1(lan port)

edit the following:

```bash
sudo nano /etc/sysctl.d/routed-ap.conf
```
and enter: <-- if vim doesn't work then use nano

```bash
net.ipv4.ip_forward=1
```

**Now we need to configure the NAT connection from Wlan0 to Wlan1**

```bash
sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE

sudo netfilter-persistent save
```


**configuring the routing**

```bash
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.bk

sudo touch /etc/dnsmasq.conf
```

in the file enter the following:

```bash
interface=wlan1
dhcp-range=10.1.1.200,10.1.1.250,255.255.255.0,72h
domain=wlan
address=/rt.wlan/10.1.1.1
```

**Creating the Access point**

```bash
sudo touch /etc/hostapd/hostapd.conf
```

enter the following:

```bash
interface=wlan1
ssid=gwart-net
hw_mode=a
channel=36
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=P!ssword123
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```

then reboot the pi

```bash
sudo reboot
``` 


## Configuring the Shard Network Drive


### Formatting and mounting the drive

**Formatting the drive:**

```bash
...
```


**finding the PARTUUID:**

```bash
sudo blkid
```


**edit the fstab:**

```bash
PARTUUID=bf5e59d4-84a1-ad40-a383-40dd8649eb27 /volume ext4 defaults 0 2
```



### Configuring Network share


installing samba
```bash
sudo apt-get install samba samba-common-bin
```


edit the file: /etc/samba/smb.conf

add the following to the buttom of the file
```bash
[PiNas]
path=/volume
writeable=yes
public=yes
```

then restart the service:

```bash
sudo systemctl restart smbd
```


## Installing Docker

```bash
sudo apt update -y

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker pi
```

## Installing docker-compose

```bash
sudo apt-get install libffi-dev libssl-dev
sudo apt install python3-dev
sudo apt-get install -y python3 python3-pip

sudo pip3 install docker-compose
```

## Installing ansible

```bash
sudo apt update -y && sudo apt install ansible
```


## Installing Xrdp

```bash
sudo apt install xrdp 

systemctl show -p SubState --value xrdp

sudo adduser xrdp ssl-cert  
```


## Install cool-retro-term

```bash
sudo apt install cool-retro-term
```
## Node Base Configurations
format the raspberry pi sd card with the following image:
2021-10-30-raspios-bullseye-arm64-lite.img

can be downloaded here: https://downloads.raspberrypi.org/raspios_arm64/images/


then once the sd card is ready then boot up the pi, and wait to you see it online on the network.

Since the pi will boot to the jared-web, i will use nmap on the jared node to see when the pi comes online, and what ip address it will recieve.

Then ssh into the pi and edit the following:

add the following to the cmdline.txt file found on the boot drive:
```bash
cgroup_memory=1 cgroup_enable=memory
```

then set the static ip address by editing the file: sudo nano /etc/dhcpcd.conf

```bash
interface wlan0
static ip_address=10.1.1.2/24
static routers=10.1.1.1
static domain_name_servers=1.1.1.1 1.0.0.1
```

then reboot the pi

--> This should be done for all nodes.

## Ansible base configurations on the cluster nodes

to harden and configure all the nodes with basic stuff such has ssh configs and fail2ban configs, you can run the playbook base-node-setup.yml

to run the playbook you will need to be in the ansible folder inside the repo and then run the command:

```bash
ansible-playbook -i inventory.ini playbooks/base-node-setup.yml
```

this will goahead and install all the security stuff for all the nodes.

If you ever need to configure a new node, then just edit the yml file or the inventory file for that specific host.


## Ansible enable iptables for all the hosts
**Manually**

run the following commands for all the nodes: 
```bash
sudo iptables -F 
sudo update-alternatives --set iptables /usr/sbin/iptables-legacy
sudo update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy
sudo reboot
```

**Ansible Magic**

You can also just run the ansible playbook config-iptables.yml


## Configuring the cluster master

ssh into the master node

run the commands:

```bash
sudo su -

curl -sfL https://get.k3s.io | K3S_KUBECONFIG_MODE="644" sh -
```

verified that it worked by running the command:

```bash
kubectl get nodes
```

before you can add other nodes you will need to get the token from the master:

```bash
sudo cat /var/lib/rancher/k3s/server/node-token
```

## Adding the rest of the nodes to the cluster

run the command to add the node to the cluster:

```bash
curl -sfL https://get.k3s.io | K3S_TOKEN="<cluster-master-token>" K3S_URL="https://10.1.1.2:6443" K3S_NODE_NAME="worker4" sh -
```

now ssh into the master and run the following command, to see if the nodes have joined the cluster:

```bash
NAME      STATUS     ROLES                  AGE     VERSION
master    Ready      control-plane,master   6m45s   v1.21.7+k3s1
worker2   Ready      <none>                 51s     v1.21.7+k3s1
worker4   NotReady   <none>                 9s      v1.21.7+k3s1
```





# New Config for Ubuntu Raspberry Pi's
cluster with docker setup:
https://medium.com/@amadmalik/installing-kubernetes-on-raspberry-pi-k3s-and-docker-on-ubuntu-20-04-ef51e5e56

portainer:
https://theselfhostingblog.com/posts/setting-up-a-kubernetes-cluster-using-raspberry-pis-k3s-and-portainer/
https://www.youtube.com/watch?v=usWCDvEAZlw


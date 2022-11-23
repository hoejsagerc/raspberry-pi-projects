on the master node:

```bash
sudo apt update
sudo apt install snapd
```

```bash
sudo reboot
```

```bash
sudo snap install core
sudo snap install helm --classic
```

```bash
kubectl -n kube-system create serviceaccount tiller
kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller

helm repo add stable https://charts.helm.sh/stable

helm repo update
helm search postgres
```
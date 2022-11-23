to install prometheus and grafana with helm run the command:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm search repo prometheus-community
```

here you will find the  chart:

prometheus-community/kube-prometheus-stack

to install:

```bash
helm install prometheus prometheus-community/kube-prometheus-stack
```

if you see this error:

```plaintext
 INSTALLATION FAILED: Kubernetes cluster unreachable: Get "http://localhost:8080/version?timeout=32s": dial tcp [::1]:8080: connect: connection refused
```

then run the command:

```bash
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
```

Then we need to change the service type for the grafana dashboard:

edit the service to NodePort

```bash
kubectl edit service prometheus-grafana
```

Then run:

```bash
kubectl get service prometheus-grafana
```

```plaintext
NAME                 TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
prometheus-grafana   NodePort   10.43.250.60   <none>        80:31671/TCP   5m18s
```

now you can access the dashboard with
¨
http://10.1.1.2:31671



default login:

username: admin
password: prom-operator
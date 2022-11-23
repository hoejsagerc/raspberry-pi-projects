# RaspberryPik3sCluster

Source Files for configuring Raspberry Pi Kubernetes Cluster


**For kube-prometheus-stack --> Look in the bottom!**

</br>


## Setting up Grafana and Prometheus for Monitoring

In this section i will walk through how to setup Grafana and Prometheus for the Raspberry Pi k3s Clsuter.

</br>

### Setting up Node Exporter on the cluster nodes

On each node run the following script:

```bash
curl -SL https://github.com/prometheus/node_exporter/releases/download/v1.0.1/node_exporter-1.0.1.linux-armv7.tar.gz > node_exporter.tar.gz && sudo tar -xvf node_exporter.tar.gz -C /usr/local/bin/ --strip-components=1
```

Then the node exporter needs to be setup as a service.

Creat the file /etc/systemd/system/nodeexporter.service

```plaintext
[Unit]
Description=NodeExporter
[Service]
TimeoutStartSec=0
ExecStart=/usr/local/bin/node_exporter
[Install]
WantedBy=multi-user.target
```

Run the commands to enable and start the service

```bash
sudo systemctl daemon-reload \
&& sudo systemctl enable nodeexporter \
&& sudo systemctl start nodeexporter
```

</br>

### Deploying Prometheus

cd in to the folder RaspberryPik3sCluster/monitoring-setup/grafana-prometheus/

Then to apply the deployment run:

```bash
kubectl apply -f prometheus.yml
```

You can check that the pods started correct with:

```bash
kubectl get pods -n monitoring
```




## KUBE-PROMETHEUS-STACK -- WORKING!

Installing the stack with helm

```bash
helm install prometheus prometheus-community/kube-prometheus-stack --namespace=prometheus --create-namespace
```

edit the following for adding nodePort to grafana
```bash
kubectl edit svc prometheus-grafana -n prometheus
``` 
change it from Cluster IP to nodePort or create an Ingress for accessing the dashboard


**Install kube-prometheus-stack:**
https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack

**Ingress config:**
https://linuxblog.xyz/posts/kube-prometheus-stack/
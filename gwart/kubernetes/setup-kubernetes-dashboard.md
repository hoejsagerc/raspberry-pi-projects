run the commands:

```bash
GITHUB_URL=https://github.com/kubernetes/dashboard/releases
VERSION_KUBE_DASHBOARD=$(curl -w '%{url_effective}' -I -L -s -S ${GITHUB_URL}/latest -o /dev/null | sed -e 's|.*/||')
sudo k3s kubectl create -f https://raw.githubusercontent.com/kubernetes/dashboard/${VERSION_KUBE_DASHBOARD}/aio/deploy/recommended.yaml
```

the add the following two files:

dashboard.admin-user.yml
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
```

dashboard.admin-user-role.yml
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
```

run the command:

```bash
sudo k3s kubectl create -f dashboard.admin-user.yml -f dashboard.admin-user-role.yml
```

then optain the bearer token and save it, this should be used as password to login everytime
```bash
sudo k3s kubectl -n kubernetes-dashboard describe secret admin-user-token | grep '^token'
```

then you will need to edit the kubernetes-dashboard service type to NodePort instead of ClusterIP

```bash
kubectl -n kubernetes-dashboard edit svc
```

then run:

```bash 
kubectl -n kubernetes-dashboard get svc
```

output
```plaintext
NAME                        TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)         AGE
dashboard-metrics-scraper   ClusterIP   10.43.105.16   <none>        8000/TCP        9m55s
kubernetes-dashboard        NodePort    10.43.98.123   <none>        443:31128/TCP   9m55s
```

notice the port for the kubernetes-dashboard. now you can access the dashboard from:

https://10.1.1.12:31128



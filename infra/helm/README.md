Place Kubernetes templates here: deployments, services, secrets, configmaps.


```bash
helm upgrade --install gigfusion . --debug -f values-hetzner.yaml --create-namespace --namespace gigfusion --set meili.createSecret=true --set meili.masterKey=YOUR_KEY
```
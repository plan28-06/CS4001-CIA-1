# Kubernetes deployment steps (screenshot each command + output)

Uses Minikube for a local cluster — simplest option for a course demo with no
real cloud account needed. If you have Docker Desktop's built-in Kubernetes
or a cloud cluster instead, the kubectl commands below are identical.

```bash
# 1. Start a local cluster
minikube start

# 2. Confirm cluster is up
kubectl get nodes

# 3. Apply the deployment and service
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# 4. Watch pods come up (screenshot once STATUS=Running for both replicas)
kubectl get pods -o wide

# 5. Confirm the deployment and service
kubectl get deployments
kubectl get services

# 6. Describe the deployment (good evidence for the report)
kubectl describe deployment traffic-app-deployment

# 7. Access the app locally (Minikube doesn't give a real external IP)
minikube service traffic-app-service --url
# then curl the printed URL, e.g.:
curl <printed-url>/
curl <printed-url>/intersections

# 8. Check logs from a pod (shows the simulated alerts firing)
kubectl logs -l app=traffic-app --tail=30

# 9. (Nice extra for "future enhancements" discussion) show scaling works
kubectl scale deployment traffic-app-deployment --replicas=3
kubectl get pods
```

Screenshot at minimum: step 4 (pods running), step 5 (deployment + service),
and step 7 (a working curl response) — that covers the "Kubernetes Deployment
Architecture" deliverable.
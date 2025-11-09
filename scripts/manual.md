# Manual Scripts

## Start Self-hosted Github Runner in Macos

## Port Forwarding for Nginx
```bash
kubectl port-forward svc/nginx-proxy -n xp 8888:80
```

## Port Forwarding for argocd
```bash
kubectl port-forward svc/argocd-server -n argocd 8081:443
```

## Get argocd Initial Admin Password
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```
Test repo for playing with Docker/k8s Passbolt installs.

Docker very straight forward.
I've installed docker, docker-compose, helm and colima via Homebrew

Note that `docker compose` is v2 and brew uses v1 of `docker-compose`

I've done manual docker, colima with kubectrl k8s and now I'm following the Helm Chart docs for Passbolt

https://www.passbolt.com/docs/hosting/configure/https/ce/docker-manual/
https://www.passbolt.com/docs/hosting/install/ce/helm-chart/


Bug(?): switching user while logged out takes you to the user recovery page (https://passbolt.local/users/recover?locale=en-UK)
another

Not a bug but a feature (request): https://community.passbolt.com/t/pb-28053-as-a-user-i-can-configure-passbolt-browser-extension-to-work-with-multiple-passbolt-instances/77
https://community.passbolt.com/t/logging-in-new-account-forces-account-recovery/3811/2

Enhancement: https://github.com/passbolt/passbolt_browser_extension/issues?q=state%3Aclosed%20label%3A%22enhancement%22%20

“Or switch to another account.” > replaced with link to a help page as you can't switch?

kubectl exec -it passbolt-69bcfd8fc8-h57rw -n passbolt -- su -c "bin/cake passbolt register_user -u me@example.com -f ‘Gareth’ -l ‘.’ -r admin" -s /bin/bash www-data

Docker image: https://hub.docker.com/r/passbolt/passbolt/

Creating k8s app secret instead of password for Fastmail:
kubectl create secret generic fastmail-smtp \
  -n passbolt \
  --from-literal=EMAIL_TRANSPORT_DEFAULT_PASSWORD=<app_password>

#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to print a message with a timestamp
log() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log "Deleting existing namespace: passbolt"
kubectl delete namespace passbolt || log "Namespace passbolt does not exist, continuing..."

log "Recreating secrets for database and SMTP"
kubectl create namespace passbolt
kubectl create secret generic passbolt-db -n passbolt \
  --from-literal=DATASOURCES_DEFAULT_PASSWORD=<password_string> \
  --from-literal=MARIADB_ROOT_PASSWORD=<password_string>

kubectl create secret generic fastmail-smtp -n passbolt \
  --from-literal=EMAIL_TRANSPORT_DEFAULT_PASSWORD=<password_string>

log "Installing Passbolt with Helm"
helm install passbolt passbolt/passbolt -f values.yaml -n passbolt --post-renderer ./inject-nodeport.py -n passbolt --set service.ports.https.nodePort=30443 --set service.ports.http.nodePort=30080

log "Retrieving pod information"
kubectl get pods -n passbolt

log "Script execution completed!"
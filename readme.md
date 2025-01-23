# Test repo for playing with Docker/k8s Passbolt installs.

Docker very straight forward.
I've installed docker, docker-compose, helm and colima via Homebrew
k9s for pod 

Note that `docker compose` is v2 and brew uses v1 of `docker-compose`

I've done manual docker, colima with kubectrl k8s and now I'm following the Helm Chart docs for Passbolt.



## injecting helm with python code needs yaml lib so do it from virtual env

### you don't need to inject python code!
leaving the pythong injection below for learning reasons but just figured out all I needed to do was port forward k8s.

[k9s](https://k9scli.io) is a great tool for easy viz and management of the k8s cluster and that's where I noticed the port forwarding optons.
Isn't learning fun?!

|Package | Version |
| --- | --- |
|pip | 24.3.1 |
|PyYAML | 6.0.2 |

```
python3 -m venv
pip3 install pyyaml
```

https://www.passbolt.com/docs/hosting/install/ce/helm-chart/
https://www.passbolt.com/docs/hosting/configure/https/ce/docker-manual/
https://www.passbolt.com/docs/hosting/install/ce/helm-chart/


### It's a feature not a bug

Bug(?): switching user while logged out takes you to the user recovery page (https://passbolt.local/users/recover?locale=en-UK)
another

Not a bug but a feature (request): https://community.passbolt.com/t/pb-28053-as-a-user-i-can-configure-passbolt-browser-extension-to-work-with-multiple-passbolt-instances/77
https://community.passbolt.com/t/logging-in-new-account-forces-account-recovery/3811/2

Enhancement: https://github.com/passbolt/passbolt_browser_extension/issues?q=state%3Aclosed%20label%3A%22enhancement%22%20

“Or switch to another account.” > replaced with link to a help page as you can't switch?

kubectl exec -it passbolt-depl-srv-7dc749fcc5-88gdx -n passbolt -- su -c "bin/cake passbolt register_user -u me@example.com -f ‘Gareth’ -l ‘.’ -r admin" -s /bin/bash www-data

Docker image: https://hub.docker.com/r/passbolt/passbolt/

Creating k8s app secret instead of password for Fastmail:
kubectl create secret generic fastmail-smtp \
  -n passbolt \
  --from-literal=EMAIL_TRANSPORT_DEFAULT_PASSWORD=<app_password>

```
#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e
kubectl delete namespace passbolt || log "Namespace passbolt does not exist, continuing..."
kubectl create namespace passbolt
kubectl create secret generic passbolt-db -n passbolt \
  --from-literal=DATASOURCES_DEFAULT_PASSWORD=<password_string> \
  --from-literal=MARIADB_ROOT_PASSWORD=<password_string>
kubectl create secret generic fastmail-smtp -n passbolt \
  --from-literal=EMAIL_TRANSPORT_DEFAULT_PASSWORD=<password_string>
helm install passbolt passbolt/passbolt -f values.yaml -n passbolt # (no longer required) --post-renderer ./inject-nodeport.py -n passbolt
kubectl get pods -n passbolt
```
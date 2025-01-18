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

Removing app password for Fastmail:
kubectl create secret generic fastmail-smtp \
  -n passbolt \
  --from-literal=EMAIL_TRANSPORT_DEFAULT_PASSWORD=<app_password>
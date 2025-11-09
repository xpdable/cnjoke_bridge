# cnjoke_bridge
A bridge to Chuck Norris jokes

## The Journey

Possibilities:

0) Existing Env:
   - Macbook M1 + Podman + Kind
   - Windows11
   - NAS Linux/GNU Synology + Docker

1) CI:
   Github + Github Action + Github Container Registry

2) CD:

  	Runtime architecture:

  	Podman/Docker compose @ macos
  	k8s in Kind @ macos
  	docker-compose @ Synology Linux
  	apline linux @ VirtualBox in macos arm64
  	apline linux @ QEMU in macos arm64
  	apline linux @ VirtualBox in Windows

- CD Runner
  Infrastructure : terraform vs ansible
  -> terraform kind provider!

  Application deployment @ github self-hosted runner

  a) Macos ARM64 Runner in macos
  - macos
  |- github runner
  |- Podman
  |- Kind Cluster
  |- application

  b) Linux ARM64 (Docker) Runner in Padman Machine
  - macos
  |- Podman
  |- github runner
  |- Kind Cluster
  |- application

  c) Linux ARM64 Docker Runner in Kind
  - macos
  |- Podman
  |- Kind Cluster
  |- github runner
  |- application




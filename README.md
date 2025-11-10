# cnjoke_bridge
A bridge to Chuck Norris jokes

Just get started [here]() if you are not interested in the trade-off journey.

## The Trade-off Journey

### 0.Challenges
- No personal public cloud resources
- No Docker Desktop
- macos @ arm64

### 1.Possibilities:

- 1.0. Existing Possible Env
   - Macbook M1 + Podman + Kind
   - Windows11
   - NAS Linux/GNU Synology + Docker

- 1.1 Continous Integration
    
    - Github + Github Action + Github Container Registry

- 1.2 Continous Deployment

    TLDR; Github + Self-hosted Runner + Podman + Kind + Helm + ArgoCD

#### Tried and Tested Options

- ✅Podman/Docker compose @ macos
- ✅k8s in Kind @ macos
- ✅docker-compose @ Synology Linux
- ❌apline linux @ VirtualBox in macos arm64
- ❌apline linux @ QEMU in macos arm64
- ⚠️apline linux @ VirtualBox in Windows

#### CD Runner
  Infrastructure : ✅terraform vs ⚠️ansible
  
    -> ✅terraform kind provider!

  ⚠️Trade-off, Podman machine runs a cloud with no default external IP

  ✅Decision: Application deployment @ github self-hosted runner @ macos

##### Tried and Tested Options
  a) ✅Macos ARM64 Runner in macos

Fastest and simplest solution for this case.
```bash
  - macos
  |- github runner
  |- Podman
      |- Kind Cluster
          |- application
```

  b) ⚠️Linux ARM64 (Docker) Runner in Padman Machine

Fesible but complex setup for certificate, and runner image setup including terraform, helm, kubectl, kind etc.
```bash
  - macos
  |- Podman
      |- github runner
      |- Kind Cluster
          |- application
```

  c) ❌Linux ARM64 Docker Runner in Kind

Not feasible as a Kind Cluster is considered as part of IaC deliveable.
```bash
  - macos
  |- Podman
      |- Kind Cluster
          |- github runner
          |- application
```

## Get Started

### Overall Architecture
![architecture](./docs/arch.drawio.png)

### Quick Start
⚠️If and only if you have also same setup in macos with M1 chipset, running Podman and Kind locally.
0) Start Podman machine if not yet started
1) Ensure your Podman machine certificate
2) Install dependencies: terraform, kubectl, helm, kind
3) Setup local self-hosted github runner in macos
4) Run CI pipeline to build and push application images to Github Container Registry
5) Run CD pipeline to deploy the application to Kind cluster in Podman
6) Enjoy the Chuck Norris jokes

### Application
With FastAPI python framework, a html page is rendered with a Chuck Norris joke grabbed from a public API.
The application, html template and style are in folder `app`.
Corresponding tests are in folder `tests`.

### Application Deployment and Continuous Integration
`Dockerfile` is build for the application image.
`Dockerfile_test` is build for the application integration test image.
These two images are built and pushed to Github Container Registry in the `[CI]` pipelines.

### Infrastructure as Code and Continuous Deployment
Terraform is used for IaC to deploy the application to a Kind cluster in Podman. 
A Kind provider is introduced to create and manage the Kind cluster from active terraform community.
ArgoCD is used for GitOps style deployment of the application to the Kind cluster.
ArgoCD aims to maintain the application in high availability with zero-downtime deployment strategy.
Application deployment manifests follows GitOps approach and are stored in folder `k8s-deployment`.
An ArgoCD application is created post Kind cluster creation to monitor the `k8s-deployment` folder and deploy the application to the Kind cluster.

### Secrets Management
Github access token is stored as Github secret for the CI pipeline to push images to Github Container Registry.
Correspondingly, kubernetes also need this token to pull the images from the registry.
In the CD pipeline, a kubernetes secret is created by injecting the stored Github access token.

### Version Control
Following the GitOps approach, git repo is the single source of truth for both application and infrastructure.
Therefore, the `k8s_deployment` folder indicates to the runtime version, i.e. `deployment_version`.
For CI pipeline, a `version.txt` is indicated to docker tag version, i.e. `docker_build_version`.
⚠️In this approach `deployment_version` and `docker_build_version` can be different. 

### Test Strategy
- Unittest is introduced to all CI pipelines to ensure code quality.
- Integration test is done by building a test image in job as ArgoCD post syncup hook.
The failed integration test will indicate ArgoCD to degraded status.

### Improve Possibilities

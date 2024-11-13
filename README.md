# L1-CloudPlatform

The purpose of this repo its to document all the steps in deploying a CloudPlatform which purpose its to deploy, manage and monitor a number of Spoke(s) OCP Clusters.

> [!CAUTION]
> Unless specified otherwise, everything contained in this repository is unsupported by Red Hat.

## Table of Contents
- [L1-CloudPlatform](#l1-cloudplatform)
  - [Table of Contents](#table-of-contents)
  - [Method of Procedure](#method-of-procedure)
    - [Step 0. Download the pre-requisites binaries](#step-0-download-the-pre-requisites-binaries)
    - [Step 1. Mirorring the OCI content for a disconnected installation using oc-mirror](#step-1-mirorring-the-oci-content-for-a-disconnected-installation-using-oc-mirror)
    - [Step 2. Mirroring the OCI content to a Centralized Customer Registry](#step-2-mirroring-the-oci-content-to-a-centralized-customer-registry)
    - [Step 3. Agent-based Installer](#step-3-agent-based-installer)
  - [Conclusions](#conclusions)
  - [Results and Problems](#results-and-problems)

## Method of Procedure

### Step 0. Download the pre-requisites binaries

- Ensure my environment has `oc-mirror` client:
```bash
curl -L https://mirror.openshift.com/pub/openshift-v4/clients/ocp/4.16.15/oc-mirror.tar.gz | tar -xz && chmod +x oc-mirror
```

- Ensure my environment has `oc` client:
```bash
curl -LO https://mirror.openshift.com/pub/openshift-v4/clients/ocp/4.16.15/openshift-client-linux-4.16.15.tar.gz && tar -xzf openshift-client-linux-4.16.15.tar.gz && chmod +x oc kubectl
```

### Step 1. Mirorring the OCI content for a [disconnected installation using oc-mirror](https://docs.openshift.com/container-platform/4.16/installing/disconnected_install/installing-mirroring-disconnected.html)

```bash
# DOCKER_CONFIG=./.docker/config.json; ./oc-mirror --config imageset-config.yml file:///mnt/c/Users/idumi/
Creating directory: home/oc-mirror-workspace/src/publish
Creating directory: home/oc-mirror-workspace/src/v2
Creating directory: home/oc-mirror-workspace/src/charts
Creating directory: home/oc-mirror-workspace/src/release-signatures
backend is not configured in imageset-config.yaml, using stateless mode
backend is not configured in imageset-config.yaml, using stateless mode
No metadata detected, creating new workspace
..redacted..
```
For any reference of the [imageset-config.yml](imageset-config.yml).

### Step 2. Mirroring the OCI content to a Centralized Customer Registry
```bash
# DOCKER_CONFIG=./.docker/config.json; ./oc-mirror --from=./mnt/d/l1-cp/ docker://registry.example:5000 
```

### Step 3. [Agent-based Installer](https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html-single/installing_an_on-premise_cluster_with_the_agent-based_installer/index#about-the-agent-based-installer)


- Generating the `oc` client:

```bash
# ./oc adm release extract --command=${HOME}/oc registry.example:5000/ocp-release:4.16.15-x86_64 -a .docker/config.json
```

- Generating the `openshift-install` client:

```bash
# ./oc adm release extract -a .docker/config.json --command=openshift-install registry.example:5000/ocp-release:4.16.15-x86_64  
```

- Generating the [workdir](./workdir/) directory structure:

```bash
# mkdir -p ${HOME}/workdir
# tree ${HOME}/workdir
.
├── agent-config.yaml
├── install-config.yaml
└── openshift
    ├── 99_01_argo_namespace.yaml
    ├── 99_02_argo_operatorgroup.yaml
    └── 99_03_argo_subscription.yaml

2 directory, 5 files
```
- Installing the 
- Generating the `.iso` content:

```bash
# ./openshift-install agent create image --dir ${HOME}/workdir/. --log-level debug
```

## Conclusions

## Results and Problems
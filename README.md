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
    - [Step 3. Downloading the RHCOS to AirGapped HTTP Server](#step-3-downloading-the-rhcos-to-airgapped-http-server)
    - [Step 4. Agent-based Installer](#step-4-agent-based-installer)
    - [Step 5. Hub Configuration](#step-5-hub-configuration)
    - [Step 6. Spoke deployment](#step-6-spoke-deployment)
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

> [!WARNING]
> Ensure to include in your `config.json` the pull-secret of your AirGapped Registry and Red Hat public [pull-secret](https://console.redhat.com/openshift/install/pull-secret).

```bash
# DOCKER_CONFIG=${HOME}/.docker/config.json; ./oc-mirror --config imageset-config.yml file:///mnt/c/Users/idumi/
Creating directory: home/oc-mirror-workspace/src/publish
Creating directory: home/oc-mirror-workspace/src/v2
Creating directory: home/oc-mirror-workspace/src/charts
Creating directory: home/oc-mirror-workspace/src/release-signatures
backend is not configured in imageset-config.yaml, using stateless mode
backend is not configured in imageset-config.yaml, using stateless mode
No metadata detected, creating new workspace
..redacted..
```
For any reference of the [imageset-config.yml](./imageset-config.yml).

> [!WARNING]
> In order to ensure that we adhere to the latest `day2-operator` channel used, ensure that your `imageset-config.yaml` content its allign the content reflected by running:
>
> ```bash
> oc-mirror list operators --catalog=registry.redhat.io/redhat/redhat-operator-index:v4.16 --package=advanced-cluster-management
> Logging to .oc-mirror.log
> NAME                         DISPLAY NAME                                DEFAULT CHANNEL
> advanced-cluster-management  Advanced Cluster Management for Kubernetes  release-2.12
> 
> PACKAGE                      CHANNEL       HEAD
> advanced-cluster-management  release-2.10  advanced-cluster-management.v2.10.6
> advanced-cluster-management  release-2.11  advanced-cluster-management.v2.11.3
> advanced-cluster-management  release-2.12  advanced-cluster-management.v2.12.0
> ```
> As outlined in the above example, the [imageset-config.yml](./imageset-config.yml) used in week46-2024 it was refering the `release-2.11` default channel for the `advanced-cluster-management`, in order to adhere to the latest changes, use the [imageset-config-w47.yml](./imageset-config-w47.yml).


### Step 2. Mirroring the OCI content to a Centralized Customer Registry
```bash
# DOCKER_CONFIG=${HOME}/.docker/config.json;  \
    ./oc-mirror --from=./mnt/d/l1-cp/ docker://registry.example:5000 
```

### Step 3. Downloading the RHCOS to AirGapped HTTP Server

The [rhcos sources for deploying Managed/Spoke(s) 4.16 Clusters](https://mirror.openshift.com/pub/openshift-v4/x86_64/dependencies/rhcos/4.16/4.16.3/) its 

Ensure that you are downloading the following content:
- [rhcos-4.16.0-x86_64-live-rootfs.x86_64.img](https://mirror.openshift.com/pub/openshift-v4/x86_64/dependencies/rhcos/4.16/4.16.3/rhcos-4.16.3-x86_64-live-rootfs.x86_64.img)
- [rhcos-4.16.0-x86_64-live.x86_64.iso](https://mirror.openshift.com/pub/openshift-v4/x86_64/dependencies/rhcos/4.16/4.16.3/rhcos-4.16.3-x86_64-live.x86_64.iso)

And store them to your AirGapped HTTP(s) Server, this content its required while configuring [multicluster-engine](./hub-config/operators-config/01_ai_config.yaml) operator.


### Step 4. [Agent-based Installer](https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html-single/installing_an_on-premise_cluster_with_the_agent-based_installer/index#about-the-agent-based-installer)


- Generating the `oc` client:

```bash
# ./oc adm release extract -a .docker/config.json \
     --command=oc registry.example:5000/ocp-release:4.16.15-x86_64 
```

- Generating the `openshift-install` client:

```bash
# ./oc adm release extract -a .docker/config.json \
     --command=openshift-install registry.example:5000/ocp-release:4.16.15-x86_64  
```

- Generating the [workingdir](./workingdir/) directory structure:

```bash
# mkdir -p ${HOME}/workingdir
# tree ${HOME}/workingdir
.
├── agent-config.yaml
├── install-config.yaml
└── openshift
    ├── 99-masters-chrony-configuration.yaml
    ├── 99_01_argo.yaml
    ├── catalogSource-cs-redhat-operator-index.yaml
    ├── disable-operatorhub.yaml
    └── imageContentSourcePolicy.yaml

2 directories, 7 files
```
Explaining all the parameters of the [install-config.yaml](./workingdir/install-config.yaml), you can use the following approach:
```bash
# ./openshift-install explain installconfig.platform.baremetal
KIND:     InstallConfig
VERSION:  v1

RESOURCE: <object>
  BareMetal is the configuration used when installing on bare metal.

FIELDS:
    apiVIP <string>
      Format: ip
      DeprecatedAPIVIP is the VIP to use for internal API communication Deprecated: Use APIVIPs

    apiVIPs <[]string>
      Format: ip
      APIVIPs contains the VIP(s) to use for internal API communication. In dual stack clusters it contains an IPv4 and IPv6 address, otherwise only one VIP

    bootstrapExternalStaticGateway <string>
      Format: ip
      BootstrapExternalStaticGateway is the static network gateway of the bootstrap node. This can be useful in environments without a DHCP server.

    bootstrapExternalStaticIP <string>
      Format: ip
      BootstrapExternalStaticIP is the static IP address of the bootstrap node. This can be useful in environments without a DHCP server.

    bootstrapOSImage <string>
      BootstrapOSImage is a URL to override the default OS image for the bootstrap node. The URL must contain a sha256 hash of the image e.g https://mirror.example.com/images/qemu.qcow2.gz?sha256=a07bd...

    bootstrapProvisioningIP <string>
      Format: ip
      BootstrapProvisioningIP is the IP used on the bootstrap VM to bring up provisioning services that are used to create the control-plane machines

    clusterOSImage <string>
      ClusterOSImage is a URL to override the default OS image for cluster nodes. The URL must contain a sha256 hash of the image e.g https://mirror.example.com/images/metal.qcow2.gz?sha256=3b5a8...

    clusterProvisioningIP <string>
      ClusterProvisioningIP is the IP on the dedicated provisioning network where the baremetal-operator pod runs provisioning services, and an http server to cache some downloaded content e.g RHCOS/IPA images

    defaultMachinePlatform <object>
      DefaultMachinePlatform is the default configuration used when installing on bare metal for machine pools which do not define their own platform configuration.

    externalBridge <string>
      External bridge is used for external communication.

    externalMACAddress <string>
      ExternalMACAddress is used to allow setting a static unicast MAC address for the bootstrap host on the external network. Consider using the QEMU vendor prefix `52:54:00`. If left blank, libvirt will generate one for you.

    hosts <[]object> -required-
      Hosts is the information needed to create the objects in Ironic.
      Host stores all the configuration data for a baremetal host.

    ingressVIP <string>
      Format: ip
      DeprecatedIngressVIP is the VIP to use for ingress traffic Deprecated: Use IngressVIPs

    ingressVIPs <[]string>
      Format: ip
      IngressVIPs contains the VIP(s) to use for ingress traffic. In dual stack clusters it contains an IPv4 and IPv6 address, otherwise only one VIP

    libvirtURI <string>
      Default: "qemu:///system"
      LibvirtURI is the identifier for the libvirtd connection.  It must be reachable from the host where the installer is run. Default is qemu:///system

    provisioningBridge <string>
      Provisioning bridge is used for provisioning nodes, on the host that will run the bootstrap VM.

    provisioningDHCPExternal <boolean>
      DeprecatedProvisioningDHCPExternal indicates that DHCP is provided by an external service. This parameter is replaced by ProvisioningNetwork being set to "Unmanaged".

    provisioningDHCPRange <string>
      ProvisioningDHCPRange is used to provide DHCP services to hosts for provisioning.

    provisioningHostIP <string>
      DeprecatedProvisioningHostIP is the deprecated version of clusterProvisioningIP. When the baremetal platform was initially added to the installer, the JSON field for ClusterProvisioningIP was incorrectly set to "provisioningHostIP."  This field is here to allow backwards-compatibility.

    provisioningMACAddress <string>
      ProvisioningMACAddress is used to allow setting a static unicast MAC address for the bootstrap host on the provisioning network. Consider using the QEMU vendor prefix `52:54:00`. If left blank, libvirt will generate one for you.

    provisioningNetwork <string>
      Default: "Managed"
      Valid Values: "","Managed","Unmanaged","Disabled"
      ProvisioningNetwork is used to indicate if we will have a provisioning network, and how it will be managed.

    provisioningNetworkCIDR <Any>
      ProvisioningNetworkCIDR defines the network to use for provisioning.

    provisioningNetworkInterface <string>
      ProvisioningNetworkInterface is the name of the network interface on a control plane baremetal host that is connected to the provisioning network.
```

- Installing the `nmstate` on the host:
```bash
# dnf -y install nmstate
```
- Generating the `.iso` content:

```bash
# ./openshift-install agent create image --dir ${HOME}/workdir/. --log-level debug
```
Once the `.iso` file has been generated, mount it to the Server(s) BMC and boot from it.

- Monitoring the installation process:
```bash
./openshift-install --dir ${HOME}/workingdir/. agent wait-for install-complete \
    --log-level=info
```
### Step 5. [Hub Configuration](https://docs.redhat.com/en/documentation/red_hat_openshift_gitops/1.12/html-single/argo_cd_applications/index)

Once the Hub Cluster OCP and `openshift-gitop-operator` are fully deploy, you can proceed by creating the Hub Configuration ArgoCD Applications:

- Label the Storage nodes of your Hub Cluster:
```bash
# oc label nodes master{0,1,2} cluster.ocs.openshift.io/openshift-storage=""
```
Ensure that the nodes that are 
- Create the [ArgoCD Applications](./hub-config/hub-operators-argoapps.yaml):
```bash
# oc create -f ./hub-config/hub-operators-argoapps.yaml
```
> [!WARNING]
> Ensure that the Git-Server values are set according to your system for [hub-operators-argoapps.yaml](./hub-config/hub-operators-argoapps.yaml).
>
> Example used: 
> ```bash
> path: hub-config/operators-deployment
> repoURL: 'git@10.23.223.72:/home/git/acm.git'
> targetRevision: master
> ```

### Step 6. [Spoke deployment](https://docs.redhat.com/en/documentation/openshift_container_platform/4.16/html/edge_computing/ztp-deploying-far-edge-sites#ztp-deploying-far-edge-sites)

In this section we are going to outline the steps required to achieve a first RHACM Managed/Spoke(s) Deployment.

Before applying the ArgoCD for managing the policies and managed clusters, ensure to patch the ArgoCD:

```bash
# oc patch argocd openshift-gitops -n openshift-gitops --type=merge --patch-file ./hub-config/argocd/argocdpatch.json
 ```
## Conclusions

## Results and Problems

- It has not created the [gitops_service_cluster.yaml](./hub-config/operators-config/gitops_service_cluster.yaml).
- Once the ODF Hub Cluster its created, ensure the following steps are done:
  
  - master nodes gets labeled as below:
```bash
# oc label nodes master{0,1,2} cluster.ocs.openshift.io/openshift-storage=""
```
  - ensure that the application disks gets cleaned up:
```bash
# sgdisk --zap-all /dev/sdb && sudo wipefs -a /dev/sdb
```
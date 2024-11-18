# AgentBasedInstaller Manifest Templater
The purpose of this its to create a template framework for generating the `install-config.yaml` , `agent-config.yaml` and the minimum CR required in `openshift/` directory for being able to deploy a Hub Cluster with AgentBasedInstaller based on `input-config.yaml` 

> [!CAUTION]
> Unless specified otherwise, everything contained in this repository is unsupported by Red Hat.

## Table of Contents

- [AgentBasedInstaller Manifest Templater](#agentbasedinstaller-manifest-templater)
  - [Table of Contents](#table-of-contents)
  - [How to run ?](#how-to-run-)
  - [Contact](#contact)

## How to run ?

*Answer:* Ensure that your environment has python3 and installed all dependencies as per [requirement.txt](./requirement.txt).

```bash
$ python3 abi-templater.py 
./workingdir/install-config.yaml generated successfully.
./workingdir/agent-config.yaml generated successfully.
./workingdir/openshift/01_openshift-gitops-operator.yaml generated successfully.
./workingdir/openshift/02_catalogsource.yaml generated successfully.
```

Generates the following structure:
```bash
[midu@LAPTOP-GFA2MKUN abi-templater]$ tree workingdir/
workingdir/
├── agent-config.yaml
├── install-config.yaml
└── openshift
    ├── 01_openshift-gitops-operator.yaml
    └── 02_catalogsource.yaml

1 directory, 4 files
```

## Contact

[midu@redhat.com](mihai@redhat.com)
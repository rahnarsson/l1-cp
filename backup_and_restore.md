# Restoring a Hub Cluster

## Overview
Restoring a hub cluster typically results in the redeployment of all connected spoke clusters. However, users may wish to restore the hub cluster without triggering the redeployment of spoke clusters. This procedure describes how to perform this operation while ensuring the integrity of connected resources.

---

## Prerequisites
1. Access to the backup hub cluster.
2. Administrative privileges to apply policies and manage BareMetalHost (BMH) resources.
3. An understanding of cluster management and OpenShift configurations.

---

## Procedure

### Step 1: Add Backup Labels to BMH Resources

1. **Identify BMH Resources**:
   Locate all BareMetalHost (BMH) resources that have the `infraenvs.agent-install.openshift.io` label.

2. **Apply the Backup Label Policy**:
   Use the following policy to add the label `cluster.open-cluster-management.io/backup=cluster-activation` to the identified BMH resources.

```yaml
---
apiVersion: policy.open-cluster-management.io/v1
kind: Policy
metadata:
  name: bmh-cluster-activation-label
  annotations:
    policy.open-cluster-management.io/description: Policy used to add the cluster.open-cluster-management.io/backup=cluster-activation label to all BareMetalHost resources
spec:
  disabled: false
  policy-templates:
    - objectDefinition:
        apiVersion: policy.open-cluster-management.io/v1
        kind: ConfigurationPolicy
        metadata:
          name: set-bmh-backup-label
        spec:
          object-templates-raw: |
            {{- /* Set cluster-activation label on all BMH resources */ -}}
            {{- $infra_label := "infraenvs.agent-install.openshift.io" }}
            {{- range $bmh := (lookup "metal3.io/v1alpha1" "BareMetalHost" "" "" $infra_label).items }}
                - complianceType: musthave
                  objectDefinition:
                    kind: BareMetalHost
                    apiVersion: metal3.io/v1alpha1
                    metadata:
                      name: {{ $bmh.metadata.name }}
                      namespace: {{ $bmh.metadata.namespace }}
                      labels:
                        cluster.open-cluster-management.io/backup: cluster-activation
            {{- end }}
          remediationAction: enforce
          severity: high
---
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: Placement
metadata:
  name: bmh-cluster-activation-label-pr
spec:
  predicates:
    - requiredClusterSelector:
        labelSelector:
          matchExpressions:
            - key: name
              operator: In
              values:
                - local-cluster
---
apiVersion: policy.open-cluster-management.io/v1
kind: PlacementBinding
metadata:
  name: bmh-cluster-activation-label-binding
placementRef:
  name: bmh-cluster-activation-label-pr
  apiGroup: cluster.open-cluster-management.io
  kind: Placement
subjects:
  - name: bmh-cluster-activation-label
    apiGroup: policy.open-cluster-management.io
    kind: Policy
---
apiVersion: cluster.open-cluster-management.io/v1beta2
kind: ManagedClusterSetBinding
metadata:
  name: default
  namespace: default
spec:
  clusterSet: default
```

3. **Verify Label Application**:
   Ensure the policy adds the label `cluster.open-cluster-management.io/backup=cluster-activation` to the relevant BMH resources.

---

### Step 2: Trigger a Backup

1. **Force a Backup Run**:
   - Delete and recreate the `BackupSchedule`.
   - OR update the `BackupSchedule` cron job to trigger an immediate run.
   - OR wait for the next scheduled backup.

2. **Validate the Backup**:
   Download the latest backup content and confirm the BMH resources are included in the `acm-resources-generic-schedule-latest` backup.

---

### Step 3: Restore the Hub Cluster

1. **Prepare the Restore YAML**:
   Use the following YAML to restore the hub cluster, ensuring the BMH status is included in the restore process.

```yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: Restore
metadata:
  name: restore-acm-bmh
  namespace: open-cluster-management-backup
spec:
  cleanupBeforeRestore: CleanupRestored
  veleroManagedClustersBackupName: latest
  veleroCredentialsBackupName: latest
  veleroResourcesBackupName: latest
  restoreStatus:
    includedResources:
      - BareMetalHosts
```

2. **Execute the Restore**:
   Apply the YAML to initiate the restore process.

3. **Validate the Restore**:
   Confirm the BMH resources have been restored with the correct status.

---


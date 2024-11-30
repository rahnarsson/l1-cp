#!/bin/bash

# List of package names
packages=(
  'advanced-cluster-management'
  'multicluster-engine'
  'topology-aware-lifecycle-manager'
  'openshift-gitops-operator'
  'odf-operator'
  'ocs-operator'
  'odf-csi-addons-operator'
  'local-storage-operator'
  'mcg-operator'
  'cluster-logging'
  'odf-prometheus-operator'
  'recipe'
  'rook-ceph-operator'
)

# Loop through each package
for package in "${packages[@]}"; do
  echo "Processing package: $package"
  
  # Example command (replace with actual logic)
  ./oc-mirror list operators --catalog registry.redhat.io/redhat/redhat-operator-index:v4.16 --package="$package"
  
  # Add additional logic here for processing the output if needed
done

echo "All packages processed."
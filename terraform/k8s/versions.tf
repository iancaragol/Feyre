terraform {
  backend "remote" {
    organization = "Feyre"

    workspaces {
      name = "k8s-workloads-ENVIRONMENT_REPLACEMENT" # CI uses sed to set the workspace - gross
    }
  }
  required_version = "=1.0.6"

  required_providers {
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.7.0"
    }
  }
}

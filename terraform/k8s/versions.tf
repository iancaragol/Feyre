terraform {
  backend "remote" {
    organization = "Feyre"

    workspaces {
      name = "k8s-workloads"
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

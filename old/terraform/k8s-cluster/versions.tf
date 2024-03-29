terraform {
  backend "remote" {
    organization = "Feyre"

    workspaces {
      name = "k8s-cluster-ENVIRONMENT_REPLACEMENT" # CI uses sed to set the workspace - gross
    }
  }

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "2.66.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "2.2.1"
    }
  }

  required_version = "=1.0.6"
}

terraform {
  backend "remote" {
    organization = "Feyre"

    workspaces {
      name = "k8s-cluster-${var.ENVIRONMENT}"
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

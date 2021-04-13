terraform {
  # Using the Azure Provider
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=2.46.0"
    }
  }
  # Using Terraform Cloud Remote Backend
  backend "remote" {
    hostname = "app.terraform.io"
    organization = "Feyre"

    workspaces {
      name = "Feyre"
    }
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
  # Ignore Auth Warnings
  skip_provider_registration = true

  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
  tenant_id       = var.tenant_id
}
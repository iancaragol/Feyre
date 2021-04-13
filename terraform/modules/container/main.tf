terraform {

  required_version = "=0.14.10"

  # Using the Azure Provider
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=2.46.0"
    }
  }
  # Using Terraform Cloud Remote Backend
  backend "remote" {
    hostname     = "app.terraform.io"
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


data "azurerm_container_registry" "acr" {
  name                = var.project_name
  resource_group_name = var.azure_resource_group
}

resource "azurerm_virtual_network" "vnet" {
  name                = "${var.project_name}_${var.project_env}_containers"
  location            = var.azure_location
  resource_group_name = var.azure_resource_group
  address_space       = ["10.2.0.0/16"]
  tags = {
    managed_by = "terraform"
  }
}

resource "azurerm_subnet" "subnet" {
  address_prefixes = [
    "10.2.0.0/24",
  ]
  name                 = "${var.project_name}_${var.project_env}_default_subnet"
  resource_group_name  = var.azure_resource_group
  virtual_network_name = azurerm_virtual_network.vnet.name

  delegation {

    name = "${var.project_name}_${var.project_env}_subnet_delegation"
    service_delegation {
      name    = "Microsoft.ContainerInstance/containerGroups"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }

  }
}

resource "azurerm_network_profile" "net_profile" {
  name                = "${var.project_name}_${var.project_env}_container_net_profile"
  location            = var.azure_location
  resource_group_name = var.azure_resource_group

  container_network_interface {
    name = "${var.project_name}_${var.project_env}_container_net_interface"

    ip_configuration {
      name      = "${var.project_name}_${var.project_env}_container_net_profile"
      subnet_id = azurerm_subnet.subnet.id
    }
  }
  tags = {
    managed_by = "terraform"
  }
}

resource "azurerm_container_group" "container_group" {
  ip_address_type     = "Private"
  network_profile_id  = azurerm_network_profile.net_profile.id
  location            = var.azure_location
  name                = "${var.project_name}_${var.project_env}"
  os_type             = "Linux"
  resource_group_name = var.azure_resource_group
  restart_policy      = "Always"
  tags = {
    managed_by = "terraform"
  }

  container {
    commands = [
      "python",
      "Feyre.py"
    ]
    cpu = var.cpu
    environment_variables = {
      "ENV" = var.project_env
      "ISS" = var.iss
    }
    image  = "${var.project_name}.azurecr.io/${var.project_name}:${var.image_tag}"
    memory = var.memory
    name   = "${var.project_name}-${var.project_env}"
    secure_environment_variables = {
      "FEYRE_TOKEN" = var.FEYRE_TOKEN
      "BUCKET_KEY"  = var.BUCKET_KEY
      "ACCESS_KEY"  = var.ACCESS_KEY
    }

    ports {
      port     = 5000
      protocol = "TCP"
    }

  }

  image_registry_credential {
    server   = "${var.project_name}.azurecr.io"
    username = var.project_name
    password = data.azurerm_container_registry.acr.admin_password
  }

}

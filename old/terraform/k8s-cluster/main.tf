# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
  # Ignore Auth Warnings
  skip_provider_registration = true

  client_secret   = var.CLIENT_SECRET
  client_id       = var.CLIENT_ID
  tenant_id       = var.TENANT_ID
  subscription_id = var.SUBSCRIPTION_ID
}

resource "azurerm_resource_group" "default" {
  name     = "${var.project_name}-${var.ENVIRONMENT}-rg"
  location = var.cloud_location

  tags = {
    created_by = "Terraform"
  }
}

resource "azurerm_kubernetes_cluster" "default" {
  name                = "${var.project_name}-${var.ENVIRONMENT}-aks"
  location            = azurerm_resource_group.default.location
  resource_group_name = azurerm_resource_group.default.name
  dns_prefix          = var.project_name

  # api_server_authorized_ip_ranges = var.allowed_ip_list
  default_node_pool {
    name            = "default"
    node_count      = var.node_count
    vm_size         = var.vm_size
    os_disk_size_gb = var.node_disk_size_gb
  }

  service_principal {
    client_id     = var.CLIENT_ID
    client_secret = var.CLIENT_SECRET
  }

  role_based_access_control {
    enabled = true
  }

  tags = {
    created_by = "Terraform"
  }
}

# Attach the K8s cluster to ACR

data "azuread_service_principal" "aks_principal" {
  application_id = var.CLIENT_ID
}

resource "azurerm_role_assignment" "acrpull_role" {
  scope                            = azurerm_container_registry.acr.id
  role_definition_name             = "AcrPull"
  principal_id                     = data.azuread_service_principal.aks_principal.id
  skip_service_principal_aad_check = true
}

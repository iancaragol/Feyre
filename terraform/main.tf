data "azurerm_container_registry" "acr" {
  name                = "feyre"
  resource_group_name = "Feyre"
}

resource "azurerm_virtual_network" "feyre_containers" {
  name                = "feyre_containers"
  location            = "centralus"
  resource_group_name = "Feyre"
  address_space       = ["10.2.0.0/16"]
}

resource "azurerm_subnet" "default" {
  name                 = "default"
  resource_group_name = "Feyre"
  virtual_network_name = azurerm_virtual_network.feyre_containers.name
  address_prefixs = ["10.2.0.0/24"]

  delegation {
    name = "delegation"

    service_delegation {
      name    = "Microsoft.ContainerInstance/containerGroups"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }
}

resource "azurerm_network_profile" "feyre_container_net_profile" {
  name                = "examplenetprofile"
  location            = "centralus"
  resource_group_name = "Feyre"

  container_network_interface {
    name = "feyre_container_net_interface"

    ip_configuration {
      name      = "feyre_container_net_profile"
      subnet_id = azurerm_subnet.default.id
    }
  }
}

# azurerm_container_group.feyre_test:
resource "azurerm_container_group" "feyre_test" {
  ip_address_type     = "Private"
  network_profile_id  = azurerm_virtual_network.feyre_containers.id
  location            = "centralus"
  name                = "feyre-test"
  os_type             = "Linux"
  resource_group_name = "Feyre"
  restart_policy      = "Always"
  tags = {
    managed_by = "terraform"
  }

  container {
    commands = [
      "python",
      "Feyre.py",
      "test",
      "false",
    ]
    cpu = 1
    environment_variables = {
      "ENV"  = "container"
      "TEST" = "True"
    }
    image  = "feyre.azurecr.io/feyre:test" # using "test" image
    memory = 2
    name   = "feyre-test"
    secure_environment_variables = {
      "FEYRE_TOKEN_TEST" = var.FEYRE_TOKEN_TEST # using "test" token
      "BUCKET_KEY"       = var.BUCKET_KEY
      "ACCESS_KEY"       = var.ACCESS_KEY
    }

    ports {
      port     = 80
      protocol = "TCP"
    }

  }

  image_registry_credential {
    server   = "feyre.azurecr.io"
    username = "feyre"
    password = data.azurerm_container_registry.acr.admin_password
  }

}

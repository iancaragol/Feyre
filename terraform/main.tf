data "azurerm_container_registry" "acr" {
  name                = "feyre"
  resource_group_name = "feyre"
}

# azurerm_container_group.feyre_test:
resource "azurerm_container_group" "feyre_test" {
  ip_address_type     = "Private"
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

    network_profile_id = "/subscriptions/10586921-4e01-4730-961b-4188fcaee088/resourceGroups/Feyre/providers/Microsoft.Network/virtualNetworks/Feyre-vnet"

  }

  image_registry_credential {
    server   = "feyre.azurecr.io"
    username = "feyre"
    password = data.azurerm_container_registry.acr.admin_password
  }

}

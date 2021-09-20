module "backend" {
  source = "./modules/containers/backend"

  # Config
  ACR_NAME = data.azurerm_container_registry.acr.name

  # Environment variables
  IMAGE_TAG   = var.IMAGE_TAG
  ENVIRONMENT = var.ENVIRONMENT
}

module "frontend" {
  source = "./modules/containers/frontend"

  # Config
  ACR_NAME = data.azurerm_container_registry.acr.name

  # Secret variables
  DISCORD_TOKEN = var.DISCORD_TOKEN
  # Environment variables
  IMAGE_TAG   = var.IMAGE_TAG
  ENVIRONMENT = var.ENVIRONMENT
}

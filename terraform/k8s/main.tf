module "cert_manager" {
  source = "./modules/cert-manager"
}

module "kong" {
  source = "./modules/kong"
}

module "monitoring" {
  source = "./modules/monitoring"
}

module "status_page" {
  source = "./modules/containers/status_page"

  # Config
  ACR_NAME = data.azurerm_container_registry.acr.name

  # Environment variables
  IMAGE_TAG = var.STATUS_PAGE_IMAGE_TAG
}

module "backend" {
  source = "./modules/containers/backend"

  # Config
  ACR_NAME = data.azurerm_container_registry.acr.name

  # Environment variables
  IMAGE_TAG   = var.BACKEND_IMAGE_TAG
  ENVIRONMENT = var.ENVIRONMENT

  # Secret variables
  REDIS_PASSWORD = var.REDIS_PASSWORD
  MONGO_URI      = var.MONGO_URI
}

module "frontend" {
  source = "./modules/containers/frontend"

  # Config
  ACR_NAME = data.azurerm_container_registry.acr.name

  # Secret variables
  DISCORD_TOKEN = var.DISCORD_TOKEN
  # Environment variables
  IMAGE_TAG   = var.FRONTEND_IMAGE_TAG
  ENVIRONMENT = var.ENVIRONMENT
}

module "redis" {
  source = "./modules/containers/redis"

  # Secret variables
  REDIS_PASSWORD = var.REDIS_PASSWORD
  # Environment variables
  ENVIRONMENT = var.ENVIRONMENT
}

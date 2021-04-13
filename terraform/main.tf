module "feyre_test" {
  source = "./modules/container"

  # Project Variables
  azure_resource_group = "Feyre"
  project_name         = "feyre"
  azure_location       = "centralus"

  # Container Resources
  cpu         = 1
  memory      = 1.5
  image_tag   = "test"
  project_env = "test"
  iss         = "false"

  # Feyre Credentials
  FEYRE_TOKEN     = var.FEYRE_TOKEN_TEST
  ACCESS_KEY      = var.ACCESS_KEY
  BUCKET_KEY      = var.BUCKET_KEY
  client_secret   = var.client_secret
  client_id       = var.client_id
  tenant_id       = var.tenant_id
  subscription_id = var.subscription_id
}

module "feyre_release" {
  source = "./modules/container"

  # Project Variables
  azure_resource_group = "Feyre"
  project_name         = "feyre"
  azure_location       = "centralus"

  # Container Resources
  cpu         = 1
  memory      = 2
  image_tag   = "test"
  project_env = "release"
  iss         = "false" # set to false for testing

  # Feyre Credentials
  FEYRE_TOKEN     = var.FEYRE_TOKEN_TEST #change to _RELEASE later on
  ACCESS_KEY      = var.ACCESS_KEY
  BUCKET_KEY      = var.BUCKET_KEY
  client_secret   = var.client_secret
  client_id       = var.client_id
  tenant_id       = var.tenant_id
  subscription_id = var.subscription_id
}

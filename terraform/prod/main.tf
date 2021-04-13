terraform {
    backend "remote" {
    hostname     = "app.terraform.io"
    organization = "Feyre"

    workspaces {
      name = "Feyre-Prod"
    }
  }
}

module "feyre_release" {
  source = "../modules/container"

  # Project Variables
  azure_resource_group = "Feyre"
  project_name         = "feyre"
  azure_location       = "centralus"

  # Container Resources
  cpu         = 1
  memory      = 2
  image_tag   = var.image_tag
  project_env = "prod"
  iss         = "false" 

  # Feyre Credentials
  FEYRE_TOKEN     = var.FEYRE_TOKEN
  ACCESS_KEY      = var.ACCESS_KEY
  BUCKET_KEY      = var.BUCKET_KEY
  client_secret   = var.client_secret
  client_id       = var.client_id
  tenant_id       = var.tenant_id
  subscription_id = var.subscription_id
}

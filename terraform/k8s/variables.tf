variable "DISCORD_TOKEN" {
  description = "The Discord Token for the Bot"
  type        = string
  sensitive   = true
}

variable "ENVIRONMENT" {
  description = "The Environment context which all containers are running in (dev/prod)"
  type        = string
  default     = "prod"
}

variable "IMAGE_TAG" {
  description = "The image tag to use for deployments"
  default     = "latest"
  type        = string
}

# Azure Creds
variable "CLIENT_SECRET" {
  type      = string
  sensitive = true
}

variable "CLIENT_ID" {
  type      = string
  sensitive = true
}

variable "TENANT_ID" {
  type      = string
  sensitive = true
}

variable "SUBSCRIPTION_ID" {
  type      = string
  sensitive = true
}

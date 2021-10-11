variable "DISCORD_TOKEN" {
  description = "The Discord Token for the Bot"
  type        = string
  sensitive   = true
}

variable "REDIS_PASSWORD" {
  description = "The password for redis"
  type        = string
  sensitive   = true
}

variable "MONGO_URI" {
  description = "The URI for mongo"
  type        = string
  sensitive   = true
}

variable "ENVIRONMENT" {
  description = "The Environment context which all containers are running in (dev/prod)"
  type        = string
  default     = "dev"
}

variable "STATUS_PAGE_HOSTNAME" {
  description = "The hostname for the status page (default is blank for prod otherwise use -dev)"
  type        = string
  default     = ""
}

variable "BACKEND_IMAGE_TAG" {
  description = "The image tag to use for backend deployments"
  type        = string
}

variable "FRONTEND_IMAGE_TAG" {
  description = "The image tag to use for frontend deployments"
  type        = string
}

variable "STATUS_PAGE_IMAGE_TAG" {
  description = "The image tag to use for status_page deployments"
  type        = string
}

# Azure Creds
variable "CLIENT_SECRET" {
  type = string
}

variable "CLIENT_ID" {
  type = string
}

variable "TENANT_ID" {
  type = string
}

variable "SUBSCRIPTION_ID" {
  type = string
}

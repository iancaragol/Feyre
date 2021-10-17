variable "IMAGE_TAG" {
  description = "The image tag to use for deployments"
  default     = "latest"
  type        = string
}

variable "ENVIRONMENT" {
  description = "The Environment context which all containers are running in (dev/prod)"
  type        = string
  default     = "prod"
}

variable "ACR_NAME" {
  description = "The name of the Azure Container Registry"
  type = string
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

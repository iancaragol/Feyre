variable "IMAGE_TAG" {
  description = "The image tag to use for deployments"
  default     = "latest"
  type        = string
}

variable "ACR_NAME" {
  description = "The name of the Azure Container Registry"
  type = string
}

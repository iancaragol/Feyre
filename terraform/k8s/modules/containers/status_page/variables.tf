variable "IMAGE_TAG" {
  description = "The image tag to use for deployments"
  default     = "latest"
  type        = string
}

variable "ACR_NAME" {
  description = "The name of the Azure Container Registry"
  type = string
}

variable "STATUS_PAGE_HOSTNAME" {
  description = "The hostname for the status page (default is blank for prod otherwise use -dev)"
  type        = string
  default     = ""
}

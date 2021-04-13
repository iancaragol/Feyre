variable "azure_resource_group" {
  type = string
}

variable "azure_location" {
  type = string
}

variable "project_name" {
  type = string
}

variable "project_env" {
  type = string
}

variable "iss" {
  type = string
}

variable "image_tag" {
  type = string
}

variable "memory" {
  type = number
}

variable "cpu" {
  type = number
}

# Credentials for Feyre

variable "FEYRE_TOKEN" {
  type = string
}

variable "BUCKET_KEY" {
  type = string
}

variable "ACCESS_KEY" {
  type = string
}

variable "client_secret" {
  type = string
}

variable "client_id" {
  type = string
}

variable "tenant_id" {
  type = string
}

variable "subscription_id" {
  type = string
}

variable "location" {
  description = "The supported Azure location where the resource deployed"
  type        = string
}

variable "environment_name" {
  description = "The name of the azd environment to be deployed"
  type        = string
}

variable "principal_id" {
  description = "The Id of the azd service principal to add to deployed keyvault access policies"
  type        = string
  default     = ""
}

variable "resource_group_name" {
  description = "RG for the deployment"
  type        = string
}

variable "virtual_network_address_space" {
  description = "The address space of the virtual network"
  type        = list(string)
}

variable "container_app_environment_subnet_address_prefixes" {
  description = "The address space of the container app environment subnet"
  type        = list(string)
}

variable "private_endpoint_subnet_address_prefixes" {
  description = "The address space of the private endpoint subnet"
  type        = list(string)
}

variable "service_api_image_name" {
  description = "The name of the service api image"
  type        = string
  default     = ""
}

variable "public_network_access_enabled" {
  description = "Whether or not public network access is enabled"
  type        = bool
  default     = true
}

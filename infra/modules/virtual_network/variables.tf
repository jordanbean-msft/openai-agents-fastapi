variable "resource_group_name" {
  description = "The name of the resource group to deploy resources into"
  type        = string
}

variable "tags" {
  description = "A list of tags used for deployed services."
  type        = map(string)
}

variable "resource_token" {
  description = "A suffix string to centrally mitigate resource name collisions."
  type        = string
}

variable "location" {
  description = "Location in which to deploy the network"
  type        = string
}

variable "address_space" {
  description = "VNET address space"
  type        = list(string)
}

variable "subnets" {
  description = "Subnets configuration"
  type = list(object({
    name               = string
    address_prefixes   = list(string)
    service_delegation = bool
    delegation_name    = string
    actions            = list(string)
    network_security_rules = list(object({
      name                       = string
      priority                   = number
      direction                  = string
      access                     = string
      protocol                   = string
      source_port_range          = string
      destination_port_ranges    = list(number)
      source_address_prefix      = string
      destination_address_prefix = string
    }))
  }))
}

variable "container_app_environment_subnet_name" {
  description = "Specifies resource name of the subnet hosting the Azure Container Apps environment."
  type        = string
}

variable "private_endpoint_subnet_name" {
  description = "Specifies resource name of the subnet hosting the private endpoints."
  type        = string
}
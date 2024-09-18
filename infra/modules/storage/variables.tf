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

variable "file_share_name" {
  description = "The name of the file share to create"
  type        = string
}

variable "subnet_id" {
  description = "The resource id of the subnet to deploy the private endpoint into"
  type        = string
}

variable "public_network_access_enabled" {
  description = "Whether or not public network access is enabled"
  type        = bool
}

variable "managed_identity_principal_id" {
  description = "The principal id of the managed identity to assign to the storage account"
  type        = string
}
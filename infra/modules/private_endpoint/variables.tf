variable "name" {
  description = "(Required) Specifies the name of the private endpoint. Changing this forces a new resource to be created."
  type        = string
}

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

variable "private_connection_resource_id" {
  description = "(Required) Specifies the resource id of the private link service"
  type        = string
}

variable "location" {
  description = "(Required) Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created."
  type        = string
}

variable "subnet_id" {
  description = "(Required) Specifies the resource id of the subnet"
  type        = string
}

variable "is_manual_connection" {
  description = "(Optional) Specifies whether the private endpoint connection requires manual approval from the remote resource owner."
  type        = string
  default     = false
}

variable "subresource_names" {
  description = "(Optional) Specifies a subresource name which the Private Endpoint is able to connect to."
  type        = list(string)
  default     = null
}

variable "request_message" {
  description = "(Optional) Specifies a message passed to the owner of the remote resource when the private endpoint attempts to establish the connection to the remote resource."
  type        = string
  default     = null
}

variable "private_dns" {
  default = {}
}

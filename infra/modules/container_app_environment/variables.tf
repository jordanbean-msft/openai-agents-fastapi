variable "location" {
  description = "The supported Azure location where the resource deployed"
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

variable "log_analytics_workspace_id" {
  description = "The id of the log analytics workspace to use."
  type        = string
}

variable "container_apps_environment_subnet_id" {
  description = "The id of the Container Apps Environment subnet id."
  type        = string
}

variable "workload_profile_name" {
  description = "The name of the workload profile to use."
  type        = string
  default     = "api"
}

variable "storage_account_name" {
  description = "The name of the storage account to use."
  type        = string
}

variable "storage_account_access_key" {
  description = "The access key of the storage account to use."
  type        = string
  sensitive   = true
}

variable "file_share_name" {
  description = "The name of the file share to use."
  type        = string
}

variable "app_insights_connection_string" {
  description = "The connection string of the application insights to use."
  type        = string
}

variable "log_analytics_workspace_customer_id" {
  description = "The customer id of the log analytics workspace to use."
  type        = string
}

variable "log_analytics_workspace_primary_shared_key" {
  description = "The primary shared key of the log analytics workspace to use."
  type        = string
  sensitive   = true
}
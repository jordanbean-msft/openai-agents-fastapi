output "container_app_environment_id" {
  description = "Specifies the resource id of the container app environment."
  value       = azurerm_container_app_environment.managed_environment.id
}

output "workload_profile_name" {
  description = "Specifies the name of the workload profile."
  value       = var.workload_profile_name
}

output "container_app_environment_storage_name" {
  description = "Specifies the name of the container app environment storage."
  value       = azurerm_container_app_environment_storage.storage.name
}
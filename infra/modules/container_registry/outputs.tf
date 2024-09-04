output "container_registry_id" {
  description = "The id of the Azure Container Registry."
  value       = azurerm_container_registry.acr.id
}

output "container_registry_name" {
  description = "The name of the Azure Container Registry."
  value       = azurerm_container_registry.acr.name
}

output "container_registry_login_server" {
  description = "The login server of the Azure Container Registry."
  value       = azurerm_container_registry.acr.login_server
}

output "container_registry_admin_username" {
  description = "The admin username of the Azure Container Registry."
  value       = azurerm_container_registry.acr.admin_username
}

output "container_registry_admin_password" {
  description = "The admin password of the Azure Container Registry."
  value       = azurerm_container_registry.acr.admin_password
  sensitive   = true
}

output "container_registry_endpoint" {
  description = "The endpoint of the Azure Container Registry."
  value       = azurerm_container_registry.acr.login_server
}
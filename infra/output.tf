output "AZURE_LOCATION" {
  value = var.location
}
output "AZURE_RESOURCE_GROUP" {
  value = var.resource_group_name
}

output "AZURE_CONTAINER_REGISTRY_ENDPOINT" {
  value = module.container_registry.container_registry_endpoint
}

output "API_CONTAINER_APP_ENDPOINT" {
  value = module.container_app.api_container_app_endpoint
}
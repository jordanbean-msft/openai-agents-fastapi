output "api_container_app_endpoint" {
  description = "The endpoint of the container app."
  value       = "https://${azurerm_container_app.container_app[var.api_container_app_name].ingress[0].fqdn}"
}
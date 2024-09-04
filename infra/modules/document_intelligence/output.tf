output "azure_cognitive_services_endpoint" {
  value = azurerm_cognitive_account.cognitive_account.endpoint
}

output "azure_cognitive_services_key" {
  value     = azurerm_cognitive_account.cognitive_account.primary_access_key
  sensitive = true
}

output "azure_search_service_name" {
  value = azurerm_search_service.search.name
}

output "azure_search_service_endpoint" {
  value = "https://{azurerm_search_service.search.name}.search.windows.net"
}


output "azure_search_service_apikey" {
  value = azurerm_search_service.search.primary_key
}



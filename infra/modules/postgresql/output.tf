output "azure_postgresql_database_name" {
  value     = azurerm_postgresql_flexible_server_database.database.name
  sensitive = true
}

output "azure_postgresql_fqdn" {
  value = azurerm_postgresql_flexible_server.psql_server.fqdn
}

output "azure_postgresql_username" {
  value     = local.psqlUserName
  sensitive = true
}

output "azure_postgresql_password" {
  value     = random_password.password[1].result
  sensitive = true
}

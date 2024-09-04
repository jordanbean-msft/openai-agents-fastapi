output "storage_account_name" {
  value     = azurerm_storage_account.storage_account.name
  sensitive = false
}

output "storage_account_id" {
  value     = azurerm_storage_account.storage_account.id
  sensitive = false
}

output "file_share_name" {
  value     = azurerm_storage_share.file_share.name
  sensitive = false
}

output "storage_account_key" {
  value     = azurerm_storage_account.storage_account.primary_access_key
  sensitive = true
}
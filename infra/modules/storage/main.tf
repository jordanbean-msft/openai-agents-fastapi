terraform {
  required_providers {
    azurerm = {
      version = "~>3.105.0"
      source  = "hashicorp/azurerm"
    }
    azurecaf = {
      source  = "aztfmod/azurecaf"
      version = "1.2.28"
    }
  }
}
# ------------------------------------------------------------------------------------------------------
# DEPLOY VIRTUAL NETWORK
# ------------------------------------------------------------------------------------------------------
resource "azurecaf_name" "vnet_name" {
  name          = var.resource_token
  resource_type = "azurerm_storage_account"
  random_length = 0
  clean_input   = true
}

resource "azurerm_storage_account" "storage_account" {
  name                            = azurecaf_name.vnet_name.result
  resource_group_name             = var.resource_group_name
  location                        = var.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  tags                            = var.tags
  public_network_access_enabled   = var.public_network_access_enabled
  allow_nested_items_to_be_public = false
}

resource "azurerm_storage_share" "file_share" {
  name                 = var.file_share_name
  storage_account_name = azurerm_storage_account.storage_account.name
  quota                = 1
}

module "private_endpoint" {
  source                         = "../private_endpoint"
  name                           = azurerm_storage_account.storage_account.name
  resource_group_name            = var.resource_group_name
  tags                           = var.tags
  resource_token                 = var.resource_token
  private_connection_resource_id = azurerm_storage_account.storage_account.id
  location                       = var.location
  subnet_id                      = var.subnet_id
  subresource_name               = "blob"
  is_manual_connection           = false
  private_dns_zone_group_name    = "default"
  private_dns_zone_group_ids     = var.private_dns_zone_group_ids
}
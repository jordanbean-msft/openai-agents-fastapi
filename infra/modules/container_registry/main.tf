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

data "azurerm_client_config" "current" {}
# ------------------------------------------------------------------------------------------------------
# DEPLOY CONTAINER REGISTRY
# ------------------------------------------------------------------------------------------------------
resource "azurecaf_name" "acr_name" {
  name          = var.resource_token
  resource_type = "azurerm_container_registry"
  random_length = 2
  clean_input   = true
}

resource "azurerm_container_registry" "acr" {
  name                          = azurecaf_name.acr_name.result
  resource_group_name           = var.resource_group_name
  location                      = var.location
  sku                           = "Premium"
  admin_enabled                 = true
  public_network_access_enabled = var.public_network_access_enabled
}

module "private_endpoint" {
  source                         = "../private_endpoint"
  name                           = azurerm_container_registry.acr.name
  resource_group_name            = var.resource_group_name
  tags                           = var.tags
  resource_token                 = var.resource_token
  private_connection_resource_id = azurerm_container_registry.acr.id
  location                       = var.location
  subnet_id                      = var.subnet_id
  subresource_name               = "registry"
  is_manual_connection           = false
  private_dns_zone_group_name    = "default"
  private_dns_zone_group_ids     = var.private_dns_zone_group_ids
}
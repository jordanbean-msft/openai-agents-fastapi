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
  admin_enabled                 = false
  public_network_access_enabled = var.public_network_access_enabled
  network_rule_bypass_option    = "AzureServices"
}

resource "azurerm_role_assignment" "managed_identity_acr_role" {
  scope                = azurerm_container_registry.acr.id
  role_definition_name = "AcrPull"
  principal_id         = var.managed_identity_principal_id
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
  subresource_names              = ["registry"]
  is_manual_connection           = false
}
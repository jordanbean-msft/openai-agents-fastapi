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
# Deploy cognitive services
# ------------------------------------------------------------------------------------------------------
resource "azurecaf_name" "cognitiveservices_name" {
  name          = "di-${var.resource_token}"
  resource_type = "azurerm_cognitive_account"
  random_length = 0
  clean_input   = true
}

resource "azurerm_cognitive_account" "cognitive_account" {
  name                          = azurecaf_name.cognitiveservices_name.result
  location                      = var.location
  resource_group_name           = var.resource_group_name
  kind                          = "FormRecognizer"
  sku_name                      = "S0"
  custom_subdomain_name         = azurecaf_name.cognitiveservices_name.result
  public_network_access_enabled = var.public_network_access_enabled
}

module "private_endpoint" {
  source                         = "../private_endpoint"
  name                           = azurerm_cognitive_account.cognitive_account.name
  resource_group_name            = var.resource_group_name
  tags                           = var.tags
  resource_token                 = var.resource_token
  private_connection_resource_id = azurerm_cognitive_account.cognitive_account.id
  location                       = var.location
  subnet_id                      = var.subnet_id
  subresource_name               = "account"
  is_manual_connection           = false
  private_dns_zone_group_name    = "default"
  private_dns_zone_group_ids     = var.private_dns_zone_group_ids
}
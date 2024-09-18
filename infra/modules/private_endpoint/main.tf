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
# DEPLOY PRIVATE ENDPOINT
# ------------------------------------------------------------------------------------------------------
resource "azurecaf_name" "private_endpoint_name" {
  name          = "${var.name}-${var.resource_token}"
  resource_type = "azurerm_private_endpoint"
  random_length = 0
  clean_input   = true
}

resource "azurerm_private_endpoint" "private_endpoint" {
  name                = azurecaf_name.private_endpoint_name.result
  location            = var.location
  resource_group_name = var.resource_group_name
  subnet_id           = var.subnet_id
  tags                = var.tags

  private_service_connection {
    name                           = "${var.name}Connection"
    private_connection_resource_id = var.private_connection_resource_id
    is_manual_connection           = var.is_manual_connection
    subresource_names              = try(var.subresource_names, null)
    request_message                = try(var.request_message, null)
  }

  lifecycle {
    ignore_changes = [
      tags,
      private_dns_zone_group # don't change the private dns zone group that Azure Policy is going to add
    ]
  }
}
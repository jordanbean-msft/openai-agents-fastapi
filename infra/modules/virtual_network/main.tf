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
  resource_type = "azurerm_virtual_network"
  random_length = 0
  clean_input   = true
}

resource "azurerm_virtual_network" "vnet" {
  name                = azurecaf_name.vnet_name.result
  address_space       = var.address_space
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = var.tags

  lifecycle {
    ignore_changes = [
      tags
    ]
  }
}

resource "azurerm_subnet" "subnet" {
  for_each = { for subnet in var.subnets : subnet.name => subnet }

  name                 = each.key
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = each.value.address_prefixes

  dynamic "delegation" {
    for_each = each.value.service_delegation == true ? [1] : []

    content {
      name = "delegation"
      service_delegation {
        name    = each.value.delegation_name
        actions = each.value.actions
      }
    }
  }
}

module "network_security_group" {
  for_each               = { for subnet in var.subnets : subnet.name => subnet }
  source                 = "../network_security_group"
  resource_group_name    = var.resource_group_name
  tags                   = var.tags
  resource_token         = var.resource_token
  location               = var.location
  network_security_rules = each.value.network_security_rules
  subnet_id              = azurerm_subnet.subnet[each.key].id
  subnet_name            = each.key
  depends_on             = [azurerm_subnet.subnet]
}
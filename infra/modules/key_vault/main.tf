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
# DEPLOY AZURE KEYVAULT
# ------------------------------------------------------------------------------------------------------
resource "azurecaf_name" "kv_name" {
  name          = var.resource_token
  resource_type = "azurerm_key_vault"
  random_length = 0
  clean_input   = true
}

resource "azurerm_key_vault" "kv" {
  name                          = azurecaf_name.kv_name.result
  location                      = var.location
  resource_group_name           = var.resource_group_name
  tenant_id                     = data.azurerm_client_config.current.tenant_id
  purge_protection_enabled      = false
  sku_name                      = "standard"
  tags                          = var.tags
  public_network_access_enabled = var.public_network_access_enabled
  enabled_for_deployment        = true
  enable_rbac_authorization     = true
  network_acls {
    bypass         = "AzureServices"
    default_action = var.public_network_access_enabled == true ? "Allow" : "Deny"
  }
}

resource "azurerm_role_assignment" "managed_identity_keyvault_secret_officer" {
  for_each             = var.access_policy_object_ids
  scope                = azurerm_key_vault.kv.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = each.value
}

resource "azurerm_role_assignment" "principal_id_keyvault_key_officer" {
  scope                = azurerm_key_vault.kv.id
  role_definition_name = "Key Vault Secrets Officer"
  principal_id         = var.principal_id
}

resource "azurerm_key_vault_secret" "secrets" {
  count        = length(var.secrets)
  name         = var.secrets[count.index].name
  value        = var.secrets[count.index].value
  key_vault_id = azurerm_key_vault.kv.id
  depends_on = [
    azurerm_role_assignment.managed_identity_keyvault_secret_officer,
    azurerm_role_assignment.principal_id_keyvault_key_officer
  ]
}

module "private_endpoint" {
  source                         = "../private_endpoint"
  name                           = azurerm_key_vault.kv.name
  resource_group_name            = var.resource_group_name
  tags                           = var.tags
  resource_token                 = var.resource_token
  private_connection_resource_id = azurerm_key_vault.kv.id
  location                       = var.location
  subnet_id                      = var.subnet_id
  subresource_names              = ["vault"]
  is_manual_connection           = false
}
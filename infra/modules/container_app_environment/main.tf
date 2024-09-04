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
    azapi = {
      source  = "Azure/azapi"
      version = "1.13.1"
    }
  }
}

resource "azurecaf_name" "container_app_environment_name" {
  name          = var.resource_token
  resource_type = "azurerm_container_app_environment"
  random_length = 0
  clean_input   = true
}

resource "azurerm_container_app_environment" "managed_environment" {
  name                           = azurecaf_name.container_app_environment_name.result
  location                       = var.location
  resource_group_name            = var.resource_group_name
  log_analytics_workspace_id     = var.log_analytics_workspace_id
  infrastructure_subnet_id       = var.container_apps_environment_subnet_id
  internal_load_balancer_enabled = false
  tags                           = var.tags
  workload_profile {
    name                  = var.workload_profile_name
    workload_profile_type = "D8"
    minimum_count         = 1
    maximum_count         = 1
  }
  lifecycle {
    ignore_changes = [
      tags
    ]
  }
}

resource "azurerm_container_app_environment_storage" "storage" {
  name                         = var.file_share_name
  container_app_environment_id = azurerm_container_app_environment.managed_environment.id
  account_name                 = var.storage_account_name
  access_key                   = var.storage_account_access_key
  share_name                   = var.file_share_name
  access_mode                  = "ReadOnly"
}

data "azurerm_resource_group" "resource_group" {
  name = var.resource_group_name
}

resource "azapi_update_resource" "app_insights_open_telemetry_integration" {
  name      = azurerm_container_app_environment.managed_environment.name
  parent_id = data.azurerm_resource_group.resource_group.id
  type      = "Microsoft.App/managedEnvironments@2023-11-02-preview"
  body = jsonencode({
    properties = {
      appInsightsConfiguration = {
        connectionString = var.app_insights_connection_string
      }
      appLogsConfiguration = {
        destination = "log-analytics"
        logAnalyticsConfiguration = {
          customerId = var.log_analytics_workspace_customer_id
          sharedKey  = var.log_analytics_workspace_primary_shared_key
        }
      }
      openTelemetryConfiguration = {
        tracesConfiguration = {
          destinations = ["appInsights"]
        }
        logsConfiguration = {
          destinations = ["appInsights"]
        }
      }
    }
  })
}
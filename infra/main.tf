locals {
  tags                                          = { azd-env-name : var.environment_name }
  sha                                           = base64encode(sha256("${var.environment_name}${var.location}${data.azurerm_client_config.current.subscription_id}"))
  resource_token                                = substr(replace(lower(local.sha), "[^A-Za-z0-9_]", ""), 0, 13)
  container_registry_admin_password_secret_name = "container-registry-admin-password"
  azure_openai_secret_name                      = "azure-openai-key"
  azure_cognitive_services_secret_name          = "azure-cognitive-services-key"
  azure_search_service_secret_name              = "azure-search-service-apikey"
  file_share_name                               = "data"
  default_container_app_image_name              = "mcr.microsoft.com/k8se/quickstart:latest"
  container_app_image_name                      = coalesce(var.service_api_image_name, local.default_container_app_image_name)
  api_container_app_name                        = "api"
  container_app_subnet_name                     = "container-app-subnet"
  container_app_subnet_nsg_name                 = "nsg-container-app-subnet"
  private_endpoint_subnet_name                  = "private-endpoint-subnet"
  private_endpoint_subnet_nsg_name              = "nsg-private-endpoint-subnet"
  api_version                                   = "v1"
}

# ------------------------------------------------------------------------------------------------------
# Deploy virtual network
# ------------------------------------------------------------------------------------------------------

module "virtual_network" {
  source              = "./modules/virtual_network"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = local.tags
  resource_token      = local.resource_token
  address_space       = var.virtual_network_address_space
  subnets = [
    {
      name                   = local.container_app_subnet_name
      address_prefixes       = var.container_app_environment_subnet_address_prefixes
      service_delegation     = true
      delegation_name        = "Microsoft.App/environments"
      actions                = ["Microsoft.Network/virtualNetworks/subnets/join/action"]
      network_security_rules = []
    },
    {
      name                   = local.private_endpoint_subnet_name
      address_prefixes       = var.private_endpoint_subnet_address_prefixes
      service_delegation     = false
      delegation_name        = ""
      actions                = []
      network_security_rules = []
    },
  ]
  container_app_environment_subnet_name = local.container_app_subnet_name
  private_endpoint_subnet_name          = local.private_endpoint_subnet_name
}

# ------------------------------------------------------------------------------------------------------
# Deploy application insights
# ------------------------------------------------------------------------------------------------------
module "application_insights" {
  source              = "./modules/application_insights"
  location            = var.location
  resource_group_name = var.resource_group_name
  environment_name    = var.environment_name
  workspace_id        = module.log_analytics.log_analytics_workspace_id
  tags                = local.tags
  resource_token      = local.resource_token
}

# ------------------------------------------------------------------------------------------------------
# Deploy log analytics
# ------------------------------------------------------------------------------------------------------
module "log_analytics" {
  source              = "./modules/log_analytics"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = local.tags
  resource_token      = local.resource_token
}

# ------------------------------------------------------------------------------------------------------
# Deploy managed identity
# ------------------------------------------------------------------------------------------------------
module "managed_identity" {
  source              = "./modules/managed_identity"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = local.tags
  resource_token      = local.resource_token
}

# ------------------------------------------------------------------------------------------------------
# Deploy storage account
# ------------------------------------------------------------------------------------------------------
module "storage_account" {
  source                        = "./modules/storage"
  location                      = var.location
  resource_group_name           = var.resource_group_name
  tags                          = local.tags
  resource_token                = local.resource_token
  file_share_name               = local.file_share_name
  subnet_id                     = module.virtual_network.private_endpoint_subnet_id
  public_network_access_enabled = var.public_network_access_enabled
  managed_identity_principal_id = module.managed_identity.user_assigned_identity_principal_id
}

# ------------------------------------------------------------------------------------------------------
# Deploy key vault
# ------------------------------------------------------------------------------------------------------
module "key_vault" {
  source              = "./modules/key_vault"
  location            = var.location
  principal_id        = var.principal_id
  resource_group_name = var.resource_group_name
  tags                = local.tags
  resource_token      = local.resource_token
  access_policy_object_ids = [
    module.managed_identity.user_assigned_identity_object_id
  ]
  secrets = [
  ]
  subnet_id                     = module.virtual_network.private_endpoint_subnet_id
  public_network_access_enabled = var.public_network_access_enabled
  managed_identity_principal_id = module.managed_identity.user_assigned_identity_principal_id
}

# ------------------------------------------------------------------------------------------------------
# Deploy container registry
# ------------------------------------------------------------------------------------------------------
module "container_registry" {
  source                        = "./modules/container_registry"
  location                      = var.location
  resource_group_name           = var.resource_group_name
  tags                          = local.tags
  resource_token                = local.resource_token
  subnet_id                     = module.virtual_network.private_endpoint_subnet_id
  public_network_access_enabled = var.public_network_access_enabled
  managed_identity_principal_id = module.managed_identity.user_assigned_identity_principal_id
}

# ------------------------------------------------------------------------------------------------------
# Deploy container app environment
# ------------------------------------------------------------------------------------------------------

module "container_app_environment" {
  source                                     = "./modules/container_app_environment"
  location                                   = var.location
  resource_group_name                        = var.resource_group_name
  tags                                       = local.tags
  resource_token                             = local.resource_token
  log_analytics_workspace_id                 = module.log_analytics.log_analytics_workspace_id
  container_apps_environment_subnet_id       = module.virtual_network.container_apps_environment_subnet_id
  storage_account_name                       = module.storage_account.storage_account_name
  storage_account_access_key                 = module.storage_account.storage_account_key
  file_share_name                            = module.storage_account.file_share_name
  app_insights_connection_string             = module.application_insights.application_insights_connection_string
  log_analytics_workspace_customer_id        = module.log_analytics.log_analytics_workspace_customer_id
  log_analytics_workspace_primary_shared_key = module.log_analytics.log_analytics_workspace_primary_shared_key
  depends_on                                 = [module.virtual_network]
}

# ------------------------------------------------------------------------------------------------------
# Deploy container app
# ------------------------------------------------------------------------------------------------------
module "container_app" {
  source                           = "./modules/container_app"
  location                         = var.location
  resource_group_name              = var.resource_group_name
  tags                             = local.tags
  resource_token                   = local.resource_token
  container_app_environment_id     = module.container_app_environment.container_app_environment_id
  log_analytics_workspace_id       = module.log_analytics.log_analytics_workspace_id
  container_registory_login_server = module.container_registry.container_registry_login_server
  managed_identity_id              = module.managed_identity.user_assigned_identity_id
  api_container_app_name           = local.api_container_app_name
  container_apps = [
    {
      name                  = local.api_container_app_name
      tags                  = { "azd-service-name" : local.api_container_app_name }
      revision_mode         = "Single"
      workload_profile_name = module.container_app_environment.workload_profile_name
      ingress = {
        external_enabled = true
        target_port      = 8000
        transport        = "http"
        traffic_weight = [
          {
            label           = "blue"
            latest_revision = true
            percentage      = 100
          }
        ]
      }
      secrets = [
      ]
      identity = {
        type         = "UserAssigned"
        identity_ids = [module.managed_identity.user_assigned_identity_id]
      }
      template = {
        volume = [
          {
            name         = module.storage_account.file_share_name
            storage_name = module.storage_account.file_share_name
            storage_type = "AzureFile"
          }
        ]
        containers = [
          {
            name   = "api"
            image  = local.container_app_image_name
            cpu    = 4
            memory = "16Gi"
            env = concat([
              {
                name  = "AZURE_OPENAI_ENDPOINT"
                value = module.openai.azure_cognitive_services_endpoint
              },
              {
                name  = "OPENAI_API_VERSION"
                value = "2024-05-01-preview"
              },
              {
                name  = "OPENAI_MODEL_ID"
                value = module.openai.azure_cognitive_services_chat_deployment_name
              },
              {
                name  = "OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED"
                value = "true"
              },
              {
                name  = "OTEL_SERVICE_NAME"
                value = var.environment_name
              },
              {
                name  = "OTEL_PYTHON_FASTAPI_EXCLUDED_URLS"
                value = "readiness,liveness,startup"
              },
            ])
            volume_mounts = [
              {
                volume_name = module.storage_account.file_share_name
                mount_path  = "/code/app/data"
              }
            ]
            liveness_probe = {
              initial_delay    = 30
              interval_seconds = 30
              path             = "/${local.api_version}/liveness"
              port             = 8000
              timeout          = 1
              transport        = "HTTP"
            }
            readiness_probe = {
              interval_seconds = 30
              path             = "/${local.api_version}/readiness"
              port             = 8000
              timeout          = 1
              transport        = "HTTP"
            }
            startup_probe = {
              interval_seconds = 10
              path             = "/${local.api_version}/startup"
              port             = 8000
              timeout          = 1
              transport        = "HTTP"
            }
          }
        ]
        http_scale_rule = [
          {
            name                = "http-scaler"
            concurrent_requests = 10
          }
        ]
        min_replicas = 1
        max_replicas = 1
      }
    }
  ]
}

# ------------------------------------------------------------------------------------------------------
# Deploy OpenAI
# ------------------------------------------------------------------------------------------------------
module "openai" {
  source                        = "./modules/open_ai"
  location                      = var.location
  resource_group_name           = var.resource_group_name
  resource_token                = local.resource_token
  tags                          = local.tags
  subnet_id                     = module.virtual_network.private_endpoint_subnet_id
  public_network_access_enabled = var.public_network_access_enabled
  managed_identity_principal_id = module.managed_identity.user_assigned_identity_principal_id
}

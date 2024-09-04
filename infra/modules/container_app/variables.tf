variable "location" {
  description = "The supported Azure location where the resource deployed"
  type        = string
}

variable "resource_group_name" {
  description = "The name of the resource group to deploy resources into"
  type        = string
}

variable "tags" {
  description = "A list of tags used for deployed services."
  type        = map(string)
}

variable "resource_token" {
  description = "A suffix string to centrally mitigate resource name collisions."
  type        = string
}

variable "log_analytics_workspace_id" {
  description = "The id of the log analytics workspace to use."
  type        = string
}

variable "container_registory_login_server" {
  description = "The container registry server."
  type        = string
}

variable "container_registry_admin_username" {
  description = "The container registry admin username."
  type        = string
}

variable "container_registry_admin_password_secret_name" {
  description = "The container registry admin password secret name."
  type        = string
}

variable "container_app_environment_id" {
  description = "The id of the Azure Container Apps environment."
  type        = string
}

variable "api_container_app_name" {
  description = "The name of the container app."
  type        = string
}

variable "container_apps" {
  description = "Specifies the container apps in the managed environment."
  type = list(object({
    name                  = string
    tags                  = optional(map(string))
    revision_mode         = optional(string)
    workload_profile_name = optional(string)
    ingress = optional(object({
      allow_insecure_connections = optional(bool)
      external_enabled           = optional(bool)
      target_port                = optional(number)
      transport                  = optional(string)
      traffic_weight = optional(list(object({
        label           = optional(string)
        latest_revision = optional(bool)
        revision_suffix = optional(string)
        percentage      = optional(number)
      })))
    }))
    dapr = optional(object({
      app_id       = optional(string)
      app_port     = optional(number)
      app_protocol = optional(string)
    }))
    identity = optional(object({
      type         = string
      identity_ids = list(string)
    }))
    secrets = optional(list(object({
      name                = string
      key_vault_secret_id = string
      identity            = string
    })))
    template = object({
      containers = list(object({
        name    = string
        image   = string
        args    = optional(list(string))
        command = optional(list(string))
        cpu     = optional(number)
        memory  = optional(string)
        env = optional(list(object({
          name        = string
          secret_name = optional(string)
          value       = optional(string)
        })))
        volume_mounts = optional(list(object({
          volume_name = string
          mount_path  = string
        })))
        liveness_probe = optional(object({
          initial_delay    = optional(number)
          interval_seconds = optional(number)
          path             = optional(string)
          port             = number
          timeout          = optional(number)
          transport        = string
        }))
        readiness_probe = optional(object({
          interval_seconds = optional(number)
          path             = string
          port             = number
          timeout          = optional(number)
          transport        = string
        }))
        startup_probe = optional(object({
          interval_seconds = optional(number)
          path             = string
          port             = number
          timeout          = optional(number)
          transport        = string
        }))
        min_replicas    = optional(number)
        max_replicas    = optional(number)
        revision_suffix = optional(string)
      }))
      volume = optional(list(object({
        name         = string
        storage_name = optional(string)
        storage_type = optional(string)
      })))
      http_scale_rule = optional(list(object({
        name                = string
        concurrent_requests = number
      })))
    })
  }))
}

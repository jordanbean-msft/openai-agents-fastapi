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

#------------------------------------------------------------------------------------------------------
# Deploy container app
#------------------------------------------------------------------------------------------------------
resource "azurerm_container_app" "container_app" {
  for_each = { for app in var.container_apps : app.name => app }

  name                         = each.key
  resource_group_name          = var.resource_group_name
  container_app_environment_id = var.container_app_environment_id
  tags                         = merge(var.tags, each.value.tags)
  revision_mode                = each.value.revision_mode
  registry {
    server               = var.container_registory_login_server
    username             = var.container_registry_admin_username
    password_secret_name = var.container_registry_admin_password_secret_name
  }
  workload_profile_name = each.value.workload_profile_name
  template {
    dynamic "container" {
      for_each = coalesce(each.value.template.containers, [])
      content {
        name    = container.value.name
        image   = container.value.image
        args    = try(container.value.args, null)
        command = try(container.value.command, null)
        cpu     = container.value.cpu
        memory  = container.value.memory
        dynamic "env" {
          for_each = coalesce(container.value.env, [])
          content {
            name        = env.value.name
            secret_name = try(env.value.secret_name, null)
            value       = try(env.value.value, null)
          }
        }
        dynamic "volume_mounts" {
          for_each = coalesce(container.value.volume_mounts, [])
          content {
            name = volume_mounts.value.volume_name
            path = volume_mounts.value.mount_path
          }
        }

        liveness_probe {
          initial_delay    = container.value.liveness_probe.initial_delay
          interval_seconds = container.value.liveness_probe.interval_seconds
          path             = container.value.liveness_probe.path
          port             = container.value.liveness_probe.port
          timeout          = container.value.liveness_probe.timeout
          transport        = container.value.liveness_probe.transport
        }
        readiness_probe {
          interval_seconds = container.value.readiness_probe.interval_seconds
          path             = container.value.readiness_probe.path
          port             = container.value.readiness_probe.port
          timeout          = container.value.readiness_probe.timeout
          transport        = container.value.readiness_probe.transport
        }
        startup_probe {
          interval_seconds = container.value.startup_probe.interval_seconds
          path             = container.value.startup_probe.path
          port             = container.value.startup_probe.port
          timeout          = container.value.startup_probe.timeout
          transport        = container.value.startup_probe.transport
        }
      }
    }
    min_replicas    = try(each.value.template.min_replicas, null)
    max_replicas    = try(each.value.template.max_replicas, null)
    revision_suffix = try(each.value.template.revision_suffix, null)

    dynamic "volume" {
      for_each = each.value.template.volume != null ? each.value.template.volume : []
      content {
        name         = volume.value.name
        storage_name = try(volume.value.storage_name, null)
        storage_type = try(volume.value.storage_type, null)
      }
    }

    dynamic "http_scale_rule" {
      for_each = each.value.template.http_scale_rule != null ? each.value.template.http_scale_rule : []
      content {
        name                = http_scale_rule.value.name
        concurrent_requests = http_scale_rule.value.concurrent_requests
      }
    }
  }

  dynamic "ingress" {
    for_each = each.value.ingress != null ? [each.value.ingress] : []
    content {
      allow_insecure_connections = try(ingress.value.allow_insecure_connections, null)
      external_enabled           = try(ingress.value.external_enabled, null)
      target_port                = ingress.value.target_port
      transport                  = ingress.value.transport

      dynamic "traffic_weight" {
        for_each = coalesce(ingress.value.traffic_weight, [])
        content {
          label           = traffic_weight.value.label
          latest_revision = traffic_weight.value.latest_revision
          revision_suffix = traffic_weight.value.revision_suffix
          percentage      = traffic_weight.value.percentage
        }
      }
    }
  }

  dynamic "secret" {
    for_each = each.value.secrets != null ? each.value.secrets : []
    content {
      name                = secret.value.name
      identity            = secret.value.identity
      key_vault_secret_id = secret.value.key_vault_secret_id
    }
  }

  identity {
    type         = each.value.identity.type
    identity_ids = each.value.identity.identity_ids
  }

  lifecycle {
    ignore_changes = [
      tags
    ]
  }
}

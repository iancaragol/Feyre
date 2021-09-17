output "resource_group_name" {
  value = azurerm_resource_group.default.name
}

output "kubernetes_cluster_name" {
  value = azurerm_kubernetes_cluster.default.name
}

output "kubernetes_cluster_full_id" {
  value = azurerm_kubernetes_cluster.default.id
}

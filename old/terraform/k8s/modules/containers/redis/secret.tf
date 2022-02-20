data "kubectl_path_documents" "redis_secret_manifest" {
  depends_on = [
    data.kubectl_file_documents.redis_namespace_manifest
  ]
  sensitive_vars = {
    REDIS_PASSWORD = "${var.REDIS_PASSWORD}"
  }
  pattern = "modules/containers/redis/secret.yaml"
}

resource "kubectl_manifest" "redis_secret" {
  depends_on = [
    data.kubectl_file_documents.redis_namespace_manifest
  ]
  count     = length(data.kubectl_path_documents.redis_secret_manifest.documents)
  yaml_body = element(data.kubectl_path_documents.redis_secret_manifest.documents, count.index)
}

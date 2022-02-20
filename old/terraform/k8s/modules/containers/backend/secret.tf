data "kubectl_path_documents" "backend_secret_manifest" {
  depends_on = [
    data.kubectl_file_documents.backend_namespace_manifest
  ]
  sensitive_vars = {
    REDIS_PASSWORD = "${var.REDIS_PASSWORD}"
    MONGO_URI      = "${var.MONGO_URI}"
  }
  pattern = "modules/containers/backend/secret.yaml"
}

resource "kubectl_manifest" "backend_secret" {
  depends_on = [
    data.kubectl_file_documents.backend_namespace_manifest
  ]
  count     = length(data.kubectl_path_documents.backend_secret_manifest.documents)
  yaml_body = element(data.kubectl_path_documents.backend_secret_manifest.documents, count.index)
}

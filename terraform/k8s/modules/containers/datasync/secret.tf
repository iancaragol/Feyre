data "kubectl_path_documents" "datasync_secret_manifest" {
  depends_on = [
    data.kubectl_file_documents.datasync_namespace_manifest
  ]
  sensitive_vars = {
    REDIS_PASSWORD = "${var.REDIS_PASSWORD}"
    MONGO_URI      = "${var.MONGO_URI}"
  }
  pattern = "modules/containers/datasync/secret.yaml"
}

resource "kubectl_manifest" "datasync_secret" {
  depends_on = [
    data.kubectl_file_documents.datasync_namespace_manifest
  ]
  count     = length(data.kubectl_path_documents.datasync_secret_manifest.documents)
  yaml_body = element(data.kubectl_path_documents.datasync_secret_manifest.documents, count.index)
}

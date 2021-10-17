data "kubectl_path_documents" "redis_deployment_manifest" {
  depends_on = [
    data.kubectl_file_documents.redis_namespace_manifest,
    data.kubectl_path_documents.redis_secret_manifest
  ]

  vars = {
    ENVIRONMENT = "${var.ENVIRONMENT}"
  }
  pattern = "modules/containers/redis/deployment.yaml"
}

resource "kubectl_manifest" "redis_deployment" {
  depends_on = [
    data.kubectl_file_documents.redis_namespace_manifest
  ]
  count     = length(data.kubectl_path_documents.redis_deployment_manifest.documents)
  yaml_body = element(data.kubectl_path_documents.redis_deployment_manifest.documents, count.index)
}
data "kubectl_file_documents" "redis_service_manifest" {
  depends_on = [
    data.kubectl_file_documents.redis_namespace_manifest
  ]
  content = file("modules/containers/redis/service.yaml")
}

resource "kubectl_manifest" "redis_service" {
  depends_on = [
    data.kubectl_file_documents.redis_namespace_manifest
  ]
  count     = length(data.kubectl_file_documents.redis_service_manifest.documents)
  yaml_body = element(data.kubectl_file_documents.redis_service_manifest.documents, count.index)
}

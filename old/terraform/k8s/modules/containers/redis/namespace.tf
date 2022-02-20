data "kubectl_file_documents" "redis_namespace_manifest" {
  content = file("modules/containers/redis/namespace.yaml")
}

resource "kubectl_manifest" "redis_namespace" {
  count     = length(data.kubectl_file_documents.redis_namespace_manifest.documents)
  yaml_body = element(data.kubectl_file_documents.redis_namespace_manifest.documents, count.index)
}

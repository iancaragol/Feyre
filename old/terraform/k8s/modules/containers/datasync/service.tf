data "kubectl_file_documents" "datasync_service_manifest" {
  depends_on = [
    data.kubectl_file_documents.datasync_namespace_manifest
  ]
  content = file("modules/containers/datasync/service.yaml")
}

resource "kubectl_manifest" "datasync_service" {
  depends_on = [
    data.kubectl_file_documents.datasync_namespace_manifest
  ]
  count     = length(data.kubectl_file_documents.datasync_service_manifest.documents)
  yaml_body = element(data.kubectl_file_documents.datasync_service_manifest.documents, count.index)
}

data "kubectl_file_documents" "status_page_service_manifest" {
  depends_on = [
    data.kubectl_file_documents.status_page_namespace_manifest
  ]
  content = file("modules/containers/status_page/service.yaml")
}

resource "kubectl_manifest" "status_page_service" {
  depends_on = [
    data.kubectl_file_documents.status_page_namespace_manifest
  ]
  count     = length(data.kubectl_file_documents.status_page_service_manifest.documents)
  yaml_body = element(data.kubectl_file_documents.status_page_service_manifest.documents, count.index)
}

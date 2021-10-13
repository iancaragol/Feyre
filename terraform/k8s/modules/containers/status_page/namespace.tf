data "kubectl_file_documents" "status_page_namespace_manifest" {
  content = file("modules/containers/status_page/namespace.yaml")
}

resource "kubectl_manifest" "status_page_namespace" {
  count     = length(data.kubectl_file_documents.status_page_namespace_manifest.documents)
  yaml_body = element(data.kubectl_file_documents.status_page_namespace_manifest.documents, count.index)
}

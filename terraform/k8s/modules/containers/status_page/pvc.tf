data "kubectl_path_documents" "status_page_pvc_manifest" {
  depends_on = [
    data.kubectl_file_documents.status_page_namespace_manifest
  ]
  pattern = "modules/containers/status_page/pvc.yaml"
}

resource "kubectl_manifest" "status_page_pvc" {
  depends_on = [
    data.kubectl_file_documents.status_page_namespace_manifest
  ]
  count     = length(data.kubectl_path_documents.status_page_pvc_manifest.documents)
  yaml_body = element(data.kubectl_path_documents.status_page_pvc_manifest.documents, count.index)
}

data "kubectl_path_documents" "status_page_ingress_manifest" {
  depends_on = [
    data.kubectl_file_documents.status_page_namespace_manifest
  ]

  vars = {
    STATUS_PAGE_HOSTNAME = "${var.STATUS_PAGE_HOSTNAME}"
  }

  pattern = "modules/containers/status_page/ingress.yaml"

}

resource "kubectl_manifest" "status_page_ingress" {
  depends_on = [
    data.kubectl_file_documents.status_page_namespace_manifest
  ]
  count     = length(data.kubectl_path_documents.status_page_ingress_manifest.documents)
  yaml_body = element(data.kubectl_path_documents.status_page_ingress_manifest.documents, count.index)
}

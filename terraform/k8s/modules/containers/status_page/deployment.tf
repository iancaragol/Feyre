data "kubectl_path_documents" "status_page_stack_manifest" {

  vars = {
    IMAGE_TAG            = "${var.IMAGE_TAG}"
    ACR_NAME             = "${var.ACR_NAME}"
    STATUS_PAGE_HOSTNAME = "${var.STATUS_PAGE_HOSTNAME}"
  }

  pattern = "modules/containers/status_page/stack.yaml"
}

resource "kubectl_manifest" "status_page_stack" {
  count     = length(data.kubectl_path_documents.status_page_stack_manifest.documents)
  yaml_body = element(data.kubectl_path_documents.status_page_stack_manifest.documents, count.index)
}

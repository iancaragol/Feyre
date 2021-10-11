data "kubectl_path_documents" "status_page_stack_manifest" {

  depends_on = [
    data.kubectl_file_documents.status_page_namespace_manifest,
    data.kubectl_path_documents.status_page_pvc_manifest
  ]

  vars = {
    IMAGE_TAG            = "${var.IMAGE_TAG}"
    ACR_NAME             = "${var.ACR_NAME}"
  }

  pattern = "modules/containers/status_page/deployment.yaml"
}

resource "kubectl_manifest" "status_page_stack" {
  count     = length(data.kubectl_path_documents.status_page_stack_manifest.documents)
  yaml_body = element(data.kubectl_path_documents.status_page_stack_manifest.documents, count.index)
}

data "kubectl_path_documents" "datasync_deployment_manifest" {
  depends_on = [
    data.kubectl_file_documents.datasync_namespace_manifest,
    data.kubectl_path_documents.datasync_secret_manifest
  ]

  vars = {
    ENVIRONMENT = "${var.ENVIRONMENT}"
    IMAGE_TAG   = "${var.IMAGE_TAG}"
    ACR_NAME    = "${var.ACR_NAME}"
  }
  pattern = "modules/containers/datasync/deployment.yaml"
}

resource "kubectl_manifest" "datasync_deployment" {
  depends_on = [
    data.kubectl_file_documents.datasync_namespace_manifest
  ]
  count     = length(data.kubectl_path_documents.datasync_deployment_manifest.documents)
  yaml_body = element(data.kubectl_path_documents.datasync_deployment_manifest.documents, count.index)
}

data "kubectl_file_documents" "cert_manager_manifests" {
  content = file("modules/cert-manager/cert-manager.yaml")
}

resource "kubectl_manifest" "cert_manager_manifest" {
  depends_on = [
    kubectl_manifest.cert_manager_namespace
  ]
  count     = length(data.kubectl_file_documents.cert_manager_manifests.documents)
  yaml_body = element(data.kubectl_file_documents.cert_manager_manifests.documents, count.index)
}

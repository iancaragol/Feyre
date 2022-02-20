data "kubectl_file_documents" "lets_encrypt_manifests" {
  content = file("modules/cert-manager/lets-encrypt.yaml")
}

resource "kubectl_manifest" "lets_encrypt_manifest" {
  depends_on = [
    kubectl_manifest.cert_manager_namespace,
    kubectl_manifest.cert_manager_manifest
  ]
  count     = length(data.kubectl_file_documents.lets_encrypt_manifests.documents)
  yaml_body = element(data.kubectl_file_documents.lets_encrypt_manifests.documents, count.index)
}

data "kubectl_file_documents" "cert_manager_namespace_manifest" {
  content = file("modules/cert-manager/namespace.yaml")
}

resource "kubectl_manifest" "cert_manager_namespace" {
  count     = length(data.kubectl_file_documents.cert_manager_namespace_manifest.documents)
  yaml_body = element(data.kubectl_file_documents.cert_manager_namespace_manifest.documents, count.index)
}

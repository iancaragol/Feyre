data "kubectl_file_documents" "datasync_namespace_manifest" {
  content = file("modules/containers/datasync/namespace.yaml")
}

resource "kubectl_manifest" "datasync_namespace" {
  count     = length(data.kubectl_file_documents.datasync_namespace_manifest.documents)
  yaml_body = element(data.kubectl_file_documents.datasync_namespace_manifest.documents, count.index)
}

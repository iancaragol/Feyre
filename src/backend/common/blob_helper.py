from os import environ
from azure.storage.blob import BlobServiceClient

class BlobHelper:
    def __init__(self):
        self.partition_key = environ.get("ENV")
        self.endpoint = environ.get("BLOB_ENDPOINT")
        self.connection_string = environ.get("STORAGE_ACCOUNT_CONNECTION_STRING")

    def create_container_client(self, container_name : str):
        """
        Returns an Azure Storage Blob Client for blob_name
        """
        blob_client = BlobServiceClient.from_connection_string(
            self.connection_string
        )

        container_client = blob_client.get_container_client(container_name)

        return container_client

    def upload_blob_from_file(self, container_name : str,  blob_name : str, blob_filepath : str):
        """
        Uploads blob to container_name
        """

        # TODO(IAN) Add some sort of error handling/retry logic here.
        # Also a good place to emit the latency to grafana
        container_client = self.create_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        try:
            with open(blob_filepath, "rb") as data:
                info = blob_client.upload_blob(data)
            return info
        except Exception as e:
            print("An exception occurred. Retrying!")
            print(str(e))

    def upload_blob_from_bytes(self, container_name : str, blob_name : str, blob : str):
        """
        Uploads blob as byte string to container_name
        """

        # TODO(IAN) Add some sort of error handling/retry logic here.
        # Also a good place to emit the latency to grafana
        container_client = self.create_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        try:
            info = blob_client.upload_blob(blob)
            return info
        except Exception as e:
            print("An exception occurred. Retrying!")
            print(str(e))

    def download_blob_as_file(self, container_name : str, blob_name : str, blob_destination : str):
        """
        Downloads blob_name from container_name to blob_destination
        """

        container_client = self.create_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        try:
            with open(blob_destination, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())
            return blob_destination
        except Exception as e:
            print("An exception occurred. Retrying!")
            print(str(e))
    
    def download_blob_as_bytes(self, container_name : str, blob_name : str):
        """
        Returns blob_name in bytes from container_name
        """

        container_client = self.create_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        try:
            data = blob_client.download_blob().readall()
            return data
        except Exception as e:
            print("An exception occurred. Retrying!")
            print(str(e))

    def list_blobs(self, container_name : str, sort_by : str, reverse : bool):
        """
        Lists all blobs in container_name sorted by sort_by and reversed if specified
        """

        container_client = self.create_container_client(container_name)
        blob_list = container_client.list_blobs()
        sorted_list = sorted(blob_list, key=lambda d: d[sort_by], reverse=reverse) 
        return sorted_list
        
# Leaving this here for easy devbox testing.
# if __name__ == "__main__":
#     bh = BlobHelper()
#     #x = bh.upload_blob("users", "test_blob_dl.txt", "C:\\Code\\test_blob_dl.txt")
#     #print(x)

#     p = b'TEST'
#     t = bh.upload_blob_from_bytes("users", "test-bytes.txt", p)

#     z = bh.list_blobs(container_name = "users", sort_by = "creation_time", reverse = True)
#     print(z)
    
#     y = bh.download_blob_as_bytes("users", "test-bytes.txt")
#     print(y)
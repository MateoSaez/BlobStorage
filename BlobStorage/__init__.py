from azure.storage.blob import ContainerClient
from azure.identity import DefaultAzureCredential

class BlobStorage:
    
    def __init__(self, storage_name, container_name) -> None:
        self.storage_name = f'https://{storage_name}.blob.core.windows.net/'
        self.container_name = container_name
        self.container_client = ContainerClient(
                                    account_url=self.storage_name, 
                                    container_name=self.container_name, 
                                    credential=DefaultAzureCredential(exclude_shared_token_cache_credential=True)
                                )
        self.subidos = 0

    def check_for_files(self, file_list, overwrite=False):
        if overwrite:
            net_list = file_list
        else:
            generator = self.container_client.list_blobs()
            blob_list = [item.name for item in generator]
            net_list = [(sp,bs) for sp, bs in file_list if not bs in blob_list]
        return net_list

    def push_blob(self, file, file_path):
        blob_client = self.container_client.get_blob_client(blob=file_path)
        blob_client.upload_blob(file, overwrite=True)
        self.subidos += 1
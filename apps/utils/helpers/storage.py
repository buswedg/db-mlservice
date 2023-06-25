import logging
from datetime import datetime, timedelta

from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from django.conf import settings

logger = logging.getLogger('custom')


def get_azure_presigned_url_or_none(filepath, **kwargs):
    """
    Returns a presigned URL to access the given file on Azure Blob Storage, or None if any of the required
    parameters are missing or an error occurred.

    Args:
        filepath (str): The file path of the file to generate a presigned URL for.
        **kwargs: Additional keyword arguments including azure_account_name, azure_container_name, and azure_account_key.

    Returns:
        str or None: The presigned URL if successful, or None if unsuccessful.
    """
    account_name = kwargs.get('azure_account_name', settings.AZURE_BLOB_ACCOUNT_NAME or None)
    container_name = kwargs.get('azure_container_name', settings.AZURE_BLOB_CONTAINER_NAME or None)
    account_key = kwargs.get('azure_account_key', settings.AZURE_BLOB_ACCOUNT_KEY or None)

    if not account_name or not account_key or not container_name:
        return None

    expiration = datetime.utcnow() + timedelta(days=1)

    try:
        sas = generate_blob_sas(
            account_name=account_name,
            container_name=container_name,
            account_key=account_key,
            blob_name=filepath,
            permission=BlobSasPermissions(read=True),
            expiry=expiration
        )

        sas_url = 'https://' + \
                  account_name + \
                  '.blob.core.windows.net/' + \
                  container_name + \
                  '/' + \
                  filepath + \
                  '?' + sas

        return sas_url

    except Exception as e:
        logger.error(f"Error generating Azure presigned URL for file {filepath}: {e}")

    return None

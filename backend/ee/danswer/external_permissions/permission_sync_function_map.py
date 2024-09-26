from collections.abc import Callable

from sqlalchemy.orm import Session

from danswer.configs.constants import DocumentSource
from danswer.db.models import ConnectorCredentialPair
from ee.danswer.external_permissions.confluence.doc_sync import confluence_doc_sync
from ee.danswer.external_permissions.confluence.group_sync import confluence_group_sync
from ee.danswer.external_permissions.google_drive.doc_sync import gdrive_doc_sync
from ee.danswer.external_permissions.google_drive.group_sync import gdrive_group_sync


# Defining the input/output types for the sync functions
SyncFuncType = Callable[
    [
        Session,
        ConnectorCredentialPair,
    ],
    None,
]

# These functions update:
# - the user_email <-> document mapping
# - the external_user_group_id <-> document mapping
# in postgres without committing
# THIS ONE IS NECESSARY FOR AUTO SYNC TO WORK
DOC_PERMISSIONS_FUNC_MAP: dict[DocumentSource, SyncFuncType] = {
    DocumentSource.GOOGLE_DRIVE: gdrive_doc_sync,
    DocumentSource.CONFLUENCE: confluence_doc_sync,
}

# These functions update:
# - the user_email <-> external_user_group_id mapping
# in postgres without committing
# THIS ONE IS OPTIONAL ON AN APP BY APP BASIS
GROUP_PERMISSIONS_FUNC_MAP: dict[DocumentSource, SyncFuncType] = {
    DocumentSource.GOOGLE_DRIVE: gdrive_group_sync,
    DocumentSource.CONFLUENCE: confluence_group_sync,
}


def check_if_valid_sync_source(source_type: DocumentSource) -> bool:
    return source_type in DOC_PERMISSIONS_FUNC_MAP
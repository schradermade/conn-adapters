def test_gdrive_adapter_exports_import() -> None:
    from adapters.gdrive import (  # noqa: F401
        BaseDocument,
        ConnectorConfig,
        GoogleDriveDocument,
        GoogleDriveSyncRequest,
        SyncRequest,
    )

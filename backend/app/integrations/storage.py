class StorageProvider:
    async def upload(self, filename: str, content_type: str, data: bytes) -> str:
        raise NotImplementedError


class LocalStorageProvider(StorageProvider):
    async def upload(self, filename: str, content_type: str, data: bytes) -> str:
        return f"local://uploads/{filename}"


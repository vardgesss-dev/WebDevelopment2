from botocore.exceptions import ClientError, BotoCoreError
from fastapi import HTTPException

from adapters.storage.base import StorageAdapter
import aioboto3


class S3StorageAdapter(StorageAdapter):
    def __init__(
        self,
        bucket: str,
        url: str,
        access_key: str,
        secret_key: str,
        region: str
    ):
        self.bucket = bucket
        self.url = url
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.session = aioboto3.Session()

    async def upload(self, content: bytes, key: str, content_type: str) -> str:
        try:
            async with self.session.client(
                "s3",
                endpoint_url=self.url,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region,
            ) as client:
                await client.put_object(
                    Bucket=self.bucket,
                    Key=key,
                    Body=content,
                    ContentType=content_type,
                )
        except (ClientError, BotoCoreError) as e:
            raise HTTPException(status_code=502, detail=str(e))

        return f"http://localhost:9000/{self.bucket}/{key}"

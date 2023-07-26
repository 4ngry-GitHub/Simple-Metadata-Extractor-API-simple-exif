from pydantic import BaseModel, Field


class MetadataOutputModel(BaseModel):
    filename: str = Field(None)
    extension: str = Field(None)
    size: str = Field(None)
    location: str = Field(None)
    device: str = Field(None)
    meta_data: dict = Field(default=dict())
    
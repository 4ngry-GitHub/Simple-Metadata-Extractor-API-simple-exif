from typing import Annotated
from decimal import Decimal

from banditsdk.common.result import Result
from fastapi import FastAPI, File, UploadFile

from config import config
from metadata_service.mde_service import extract_data, get_google_maps_url, clear_metadata_from_image

app = FastAPI(title="MD-Extractor API", version=config.api_version)
# TODO: close file if possible.


@app.get("/get-coord-link")
async def get_googlemap_link(latitude: float, longitude: float) -> Result:
    return Result.success(get_google_maps_url(latitude, longitude))


@app.post("/md-extract/", description="Extract metadata from image. Allowed formats: JPG, HEIC.")
async def extract_metadata(image: UploadFile) -> Result:
    if not image.headers.get("content-type") == "image/jpeg" or image.headers.get("content-type") == "image/heic":
        return Result.failure(error="Invalid image format.")
    
    result = extract_data(image.file)
    if result.is_success():
        updated_data = result.data
        updated_data.filename = image.filename
        updated_data.extension = image.headers.get("content-type")
        updated_data.size = f"{image.size} Bytes"
        return Result.success(data=updated_data)
    return result


@app.post("/md-erase/", description="Erase metadata from image. Allowed formats: JPG, HEIC.")
async def erase_metadata(image: UploadFile) -> Result:
    if not image.headers.get("content-type") == "image/jpeg" or image.headers.get("content-type") == "image/heic":
        return Result.failure(error="Invalid image format.")
    
    result = clear_metadata_from_image(image.file)
    return result

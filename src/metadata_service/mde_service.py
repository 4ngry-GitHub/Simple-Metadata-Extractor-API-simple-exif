from banditsdk.common.result import Result
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS

from common.log_helper import get_logger
from metadata_service.md_model import MetadataOutputModel
# PIL module name: Pillow


def convert_decimal_degrees(degree, minutes, seconds, direction):
    decimal_degrees = degree + minutes / 60 + seconds / 3600
    if direction == "S" or direction == "W":
        decimal_degrees *= -1
    return decimal_degrees


def create_google_maps_url(gps_coords):            
    dec_deg_lat = convert_decimal_degrees(float(gps_coords["lat"][0]),  float(gps_coords["lat"][1]), float(gps_coords["lat"][2]), gps_coords["lat_ref"])
    dec_deg_lon = convert_decimal_degrees(float(gps_coords["lon"][0]),  float(gps_coords["lon"][1]), float(gps_coords["lon"][2]), gps_coords["lon_ref"])
    return f"https://maps.google.com/?q={dec_deg_lat},{dec_deg_lon}"


def get_google_maps_url(latitude, longitude):
    return f"https://maps.google.com/?q={latitude},{longitude}"


def extract_data(file, logger = get_logger()) -> Result:
    try:
        image = Image.open(file)
        logger.info(str(file) + " - has been opened.")
        gps_coords = {}
        if image._getexif() == None:
            return Result.failure(error="File doesn`t contains data to extract.")
        else:
            exif_model = MetadataOutputModel()

            for tag, value in image._getexif().items():
                tag_name = TAGS.get(tag)
                if tag_name == "GPSInfo":
                    for key, val in value.items():
                        print(f"{GPSTAGS.get(key)} - {val}")
                        if GPSTAGS.get(key) == "GPSLatitude":
                            gps_coords["lat"] = val
                        elif GPSTAGS.get(key) == "GPSLongitude":
                            gps_coords["lon"] = val
                        elif GPSTAGS.get(key) == "GPSLatitudeRef":
                            gps_coords["lat_ref"] = val
                        elif GPSTAGS.get(key) == "GPSLongitudeRef":
                            gps_coords["lon_ref"] = val   
                else:
                    exif_model.meta_data[str(tag_name)] = str(value)
            if gps_coords:
                exif_model.location = create_google_maps_url(gps_coords)
        return Result.success(data=exif_model)
    except IOError:
        logger.error("IOError | File format not supported!")
        return Result.failure(error="File format is not supported!")


def clear_metadata_from_image(file, logger = get_logger()) -> Result:
    try:
        image = Image.open(file)
        logger.info(str(file) + " - has been opened.")
        image._exif = None
        image.info = None
        # TODO: this will cause an error. Need different solution to return image.
        return Result.success(bytes(image))
    except IOError:
        logger.error("IOError | File format not supported!")
        return Result.failure(error="File format not supported!")
    except Exception:
        logger.error("Unhandled error has been occurred.")
        return Result.server_error()
    
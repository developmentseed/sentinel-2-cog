"""Sentinel-s2-l1c to COG: Handler."""

import os
import logging

from boto3.session import Session as boto3_session

from rio_tiler.sentinel2 import _sentinel_parse_scene_id
from rio_cogeo.cogeo import cog_translate


logger = logging.getLogger("sentinel2_to_cog")
logger.setLevel(logging.INFO)

session = boto3_session()
s3 = session.client("s3")

BUCKET = os.environ["OUTPUT_BUCKET"]
PREFIX = os.environ.get("OUTPUT_PREFIX", "sentinel-s2-l1c")


def main(event, context):
    """Handler."""
    logger.info(event)

    sceneid = event["sceneid"]
    band = event["band"]

    scene_params = _sentinel_parse_scene_id(sceneid)
    band_key = f"{scene_params['key']}/B{band}.jp2"

    logger.info(f"Downloading {band_key}")
    src_path = f"/tmp/{band}.jp2"
    with open(src_path, "wb") as f:
        s3.download_fileobj(
            "sentinel-s2-l1c", band_key, f, ExtraArgs={"RequestPayer": "requester"}
        )

    logger.info(f"Translating {band_key} to COG")
    config = dict(NUM_THREADS=100, GDAL_TIFF_OVR_BLOCKSIZE=128)

    output_profile = {
        "driver": "GTiff",
        "interleave": "pixel",
        "tiled": True,
        "blockxsize": 256,
        "blockysize": 256,
        "compress": "DEFLATE",
    }

    cog_path = f"/tmp/{band}.tif"
    cog_translate(
        src_path,
        cog_path,
        output_profile,
        nodata=0,
        in_memory=False,
        config=config,
        quiet=True,
    )

    params = {
        "ACL": "public-read",
        "Metadata": {"scene": sceneid, "bands": band},
        "ContentType": "image/tiff",
    }

    key = band_key.replace(".jp2", ".tif")
    if PREFIX:
        key = f"{PREFIX}/{key}"

    logger.info(f"Uploading {key}")
    with open(cog_path, "rb") as data:
        s3.upload_fileobj(data, BUCKET, key, ExtraArgs=params)

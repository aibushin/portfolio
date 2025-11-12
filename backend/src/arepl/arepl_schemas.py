from arepl_dump import dump  # type: ignore  # noqa: F401
import sys

sys.path.append("/app")
from src.api.schemas import OFDReceiptSchema
import orjson
import os

files_path = "/app/tests/mocks/ofd_responses_raw"

json_files = [file for file in os.listdir(files_path) if file.endswith(".json")]
receipts = {}
receipt_schemas = []

for json_file in json_files:
    with open(os.path.join(files_path, json_file), "r") as f:
        data = orjson.loads(f.read())
        receipts[json_file] = data
        receipt_schemas.append(
            OFDReceiptSchema(**data["request"], **data["data"]["json"])
        )


# receipt_schema = OFDReceiptSchema()

import json
import pathlib

import typer

from miappe.metadata.io import MetadataIO
from miappe.metadata.validator import create_sheet_validator, validation_sheets

app = typer.Typer()


@app.command()
def validate(path: pathlib.Path, value_index: int = 3):
    try:
        MetadataIO(path, value_index)
    except ValueError:
        raise


@app.command()
def export_schema(
        path: pathlib.Path = pathlib.Path("."),
        indent: int = 2):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
    category = validation_sheets
    for item in category:
        model = create_sheet_validator(item)
        json_schema = model.model_json_schema()
        filename = item.lower().strip().replace(" ", "_") + "_schema.json"
        with open(path / filename, "w") as file:
            json.dump(json_schema, file, indent=indent)


if __name__ == "__main__":
    app()

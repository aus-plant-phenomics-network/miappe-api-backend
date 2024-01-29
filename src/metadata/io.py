import numpy as np
import pandas as pd

from src.metadata.helpers import validation_sheets
from src.metadata.validator import create_sheet_validator


class MetadataIO:
    categories = validation_sheets
    validation_models = {cat: create_sheet_validator(cat) for cat in categories}

    def __init__(self, path: str, value_index: int = 3, validate: bool = True):
        self.path = path
        self.value_index = value_index
        self.frames = self.read_excel()
        if validate:
            for cat in self.categories:
                self.validate(cat)

    def _read_investigation(self) -> pd.DataFrame:
        df = pd.read_excel(self.path, sheet_name="Investigation", index_col=0).T
        return df.loc[["Value"], :]

    def _read_non_investigation(self, category: str) -> pd.DataFrame:
        df = pd.read_excel(self.path, sheet_name=category)
        df.drop(columns="Field", inplace=True)
        return df.iloc[self.value_index:, :]

    def read_excel(self) -> dict[str, pd.DataFrame]:
        frames = {}
        for cat in self.categories:
            df = self._read_investigation() if cat == "Investigation" else self._read_non_investigation(cat)
            df = df.replace(np.nan, None)
            df.columns = [col.strip().replace('*', '') for col in df.columns]
            frames[cat] = df
        return frames

    def validate(self, category: str) -> None:
        model = self.validation_models[category]
        data = self.frames[category]
        if isinstance(data, pd.Series):
            data = [data.to_dict()]
        else:
            data = data.to_dict(orient="records")
        for item in data:
            try:
                model(**item)
            except ValueError as e:
                print(e)

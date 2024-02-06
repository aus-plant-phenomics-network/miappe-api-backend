import numpy as np
import pandas as pd
import pathlib
from miappe.metadata.helpers import validation_sheets
from miappe.metadata.validator import create_sheet_validator


class MetadataIO:
    categories = validation_sheets
    validation_models = {cat: create_sheet_validator(cat) for cat in categories}

    def __init__(self, path: str | pathlib.Path, value_index: int = 3, validate: bool = True):
        """
        Metadata class representing metadata read from a MIAPPE metadata file.

        :param path: path to MIAPPE metadata file
        :param value_index: only relevant for non-investigation sheet - row where
        first input value is provided. Based on the MIAPPE template example, the
        firs and second rows are definitions and example; the third row is where
        the first value is recorded
        :param validate: whether to validate the metadata using pydantic model
        """
        self.path = path
        self.value_index = value_index
        self.frames = self.read_excel()
        if validate:
            for cat in self.categories:
                self.validate(cat)

    def _read_investigation(self) -> pd.DataFrame:
        """
        Read investigation sheet structure and convert to dataframe
        :return: pd.DataFrame
        """
        try:
            df = pd.read_excel(self.path, sheet_name="Investigation", index_col=0, dtype=str).T
        except Exception:
            raise ValueError(f"Invalid path or file does not exist: {self.path}")
        return df.loc[["Value"], :]

    def _read_non_investigation(self, category: str) -> pd.DataFrame:
        """
        Read non-investigation sheet structure and convert to dataframe
        :param category: non investigation sheet - i.e. study, experimental factor
        :return: pd.DataFrame
        """
        df = pd.read_excel(self.path, sheet_name=category, dtype=str)
        df.drop(columns="Field", inplace=True)
        return df.iloc[self.value_index:, :]

    def read_excel(self) -> dict[str, pd.DataFrame]:
        """
        Read MIAPPE metadata file provided as an excel file
        :return: a dictionary with key being the sheet/category and value being the
        corresponding dataframe

        """
        frames = {}
        for cat in self.categories:
            df = self._read_investigation() if cat == "Investigation" else (
                self._read_non_investigation(
                    cat
                ))
            df = df.replace(np.nan, None)
            df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
            df.columns = [col.lower().strip().replace('*', '').replace(" ", "_") for col in df.columns]
            frames[cat] = df
        return frames

    def validate(self, category: str) -> None:
        """
        Use pydantic validation model to validate the matching dataframe

        :param category: sheet/category - i.e. study, investigation, experimental
        design
        :return: raise ValueError if encountered
        """
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

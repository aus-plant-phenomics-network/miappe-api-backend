from pydantic import BaseModel
from typing import Optional
import datetime


class InvestigationModel(BaseModel):
    id: Optional[str]
    title: str
    description: Optional[str]
    submission_date: Optional[datetime.datetime]
    public_release_date: Optional[datetime.datetime]
    license: Optional[str]
    miappe_version: float
    association_publication: Optional[list[str]]




from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from typing import AnyStr, Dict, List, Union


class Job(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    status: AnyStr = "in_progress"
    message: AnyStr = ""


class SearchForm(BaseModel):
    by: str = None
    value: str = None
    conditions: list[dict[str, list[str]]] = None


    class Config:
        schema_extra = {
            "example": {
                "conditions": [
                    {
                        "token": ["have"],
                        "pos": ["AUX"]
                    }
                ]
            }
        }

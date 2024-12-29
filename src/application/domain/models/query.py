from typing import Optional, Union
from pydantic import BaseModel, ConfigDict, Field, root_validator, StrictStr
from pydantic.class_validators import validator
from ..utils import TypeOpDate
from datetime import timedelta


class QueryModel(BaseModel):
    page: int = Field(1)
    limit: int = Field(100)
    sort: str = Field("created_at")
    sort_direction: int = Field(1)
    created_at: Optional[Union[TypeOpDate, StrictStr]] = None
    updated_at: Optional[Union[TypeOpDate, StrictStr]] = None

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    @root_validator(skip_on_failure=True)
    def sort_validator(cls, values):
        if values["sort"][0] == "-":
            values["sort"] = values["sort"].replace("-", "")
            values["sort_direction"] = -1
        return values

    @validator("created_at", "updated_at")
    def DateOpvalidator(cls, v: str):
        lista = []
        for index in v:
            date = TypeOpDate.value_validation(index, False)
            if TypeOpDate.value_validation(index, False):
                lista.append(TypeOpDate("gte:" + index))
                lista.append(
                    TypeOpDate("lt:" + (date + timedelta(days=1)).strftime("%Y-%m-%d"))
                )
            elif TypeOpDate.validate_format(index):
                lista.append(TypeOpDate(index))
            else:
                raise ValueError("invalid format")
        return lista

    @validator("page", "limit", "sort", "sort_direction", pre=True)
    def sort_conversion(cls, v):
        if isinstance(v, list) and v:
            return v[0]
        return v

    def query_dict(cls):
        temp = cls.model_dump(
            by_alias=True, exclude={"page", "limit", "sort", "sort_direction"}
        )
        query = {"query": {i: temp[i] for i in temp if temp[i] is not None}}
        return {
            **query,
            **cls.model_dump(
                by_alias=True, include={"page", "limit", "sort", "sort_direction"}
            ),
        }

from typing import Optional, Union
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
    field_validator,
    StrictStr,
)
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

    @model_validator(mode="after")
    def sort_validator(self):
        if self.sort[0] == "-":
            self.sort = self.sort.replace("-", "")
            self.sort_direction = -1
        return self

    @field_validator("created_at", "updated_at")
    @classmethod
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

    @field_validator("page", "limit", "sort", "sort_direction", mode="before")
    @classmethod
    def sort_conversion(cls, v):
        if isinstance(v, list) and v:
            return v[0]
        return v

    def query_dict(self):
        temp = self.model_dump(
            by_alias=True, exclude={"page", "limit", "sort", "sort_direction"}
        )
        filters = {"like": {}, "query": {}}
        for i in temp:
            if temp[i] is not None:
                if isinstance(temp[i], str) and (
                    temp[i][0] == "*" or temp[i][-1] == "*"
                ):
                    filters["like"][i] = temp[i].replace("*", "%")
                else:
                    filters["query"][i] = temp[i]
        return {
            **filters,
            **self.model_dump(
                by_alias=True, include={"page", "limit", "sort", "sort_direction"}
            ),
        }

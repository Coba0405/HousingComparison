from pydantic import BaseModel, field
from typing import Literal, Optional, List

Mode = Literal["rent", "house", "condo"]
Resion = Literal[
    "東京大都心部",
    "関東地価集中地域",
    "地方都市地価集中地域",
    "地方地価集中地域",
    "地方地域",
    "地方過疎地域",
]

class BaseRequest(BaseModel):
    horizon_years: int = Field(ge=1, le=50)
    region: Resion
    rounding_rule: Literal["round", "floor", "ceil"] = "round"

class RentRequest(BaseRequest):
    mode: Literal

from pydantic import BaseModel, Field, ValidationError
from typing import Literal, List, Optional

Mode = Literal["rent", "house", "condo"]
Region = Literal[
    "東京大都心部",
    "関東地価集中地域",
    "地方都市地価集中地域",
    "地方地価集中地域",
    "地方地域",
    "地方過疎地域",
]

class BaseRequest(BaseModel):
    horizon_years: int = Field(ge=1, le=50)
    rounding_rule: Literal["round", "floor", "ceil"] = "round"

class RentRequest(BaseRequest):
    mode: Literal["rent"] = "rent"
    rent_monthly: int = Field(ge=0)
    renewal_interval_years: int = 2
    renewal_fee_amount: int = Field(ge=0)
    contents_insurance_interval_years: int = 2
    contents_insurance_amount: int = Field(ge=0)

class OwnerCommon(BaseRequest):
    home_price: int = Field(ge=0)
    loan_years: int = Field(ge=1, le=50)
    loan_annual_rate: float = Field(ge=0.0)
    fire_insurance_monthly: int = Field(ge=0)
    property_tax_charge_month: int = Field(ge=1, le=12, default=12)

class HouseRequest(OwnerCommon):
    mode: Literal["house"] = "house"
    house_renovation_every_10y_amount: int = Field(ge=0)
    house_renovation_change_month: int = Field(ge=1, le=12, default=12)

class CondoRequest(OwnerCommon):
    mode: Literal["condo"] = "condo"
    mgmt_monthly0: int = Field(ge=0)
    reserve_monthly0: int = Field(ge=0)
    mgmt_increase_every_5y_pct: float = Field(ge=0.0)
    reserve_increase_every_5y_pct: float = Field(ge=0.0)

class YearRow(BaseModel):
    year: int
    rent: int = 0
    renewal_fee: int = 0
    contents_insurance: int = 0
    loan_payment: int = 0
    fire_insurance: int = 0
    property_taxes: int = 0
    house_renovation: int = 0
    mgmt_fee: int = 0
    reserve_fee: int = 0
    total_cost_year: int
    cum_total_cost: int

class SimulationResponse(BaseModel):
    mode: Mode
    region: Optional[Region] = None
    years: int
    rows: List[YearRow]

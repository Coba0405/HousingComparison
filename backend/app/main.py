# CORSでフロントからのアクセスを許可
# エンドポイントをモード別にわけ、I/Oの明快さを優先

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import ALLWED_ORIGINS
from .models import RentRequest, HouseRequest, CondoRequest,SimulationResponse, YearRow
from .services.simulation import simulate_rent, simulate_house, simulate_condo

app = FastAPI(title="Lease vs Own Simulator v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLWED_ORIGINS,
    allow_credentials=True, allow_mothods=["*"], allow_hoeders=["*"]
)

@app.post("/simulate_rent", response_model=SimulationResponse)
def simulate_rent_api(req: RentRequest):
    rows = simulate_rent(req)
    return SimulationResponse(mode="rent", region=req.region, years=req.horizon_years, rows=[YearRow(**r) for r in rows])

@app.post("/simulate/house", response_model=SimulationResponse)
def simulate_house_api(req: HouseRequest):
    rows = simulate_house(req)
    return SimulationResponse(mode="house", region=req.region, years=req.horizon_years, rows=[YearRow(**r) for r in rows])

@app.post("simulate/condo", response_model=SimulationResponse)
def simulate_condo_api(req: CondoRequest):
    rows = simulate_condo(req)
    return SimulationResponse(mode="condo", region=req.region, years=req.horizon_years, rows=[YearRow(**r) for r in rows])

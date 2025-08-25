# CORSでフロントからのアクセスを許可
# エンドポイントをモード別にわけ、I/Oの明快さを優先

from flask import Flask, request, jsonify
from flask_cors import CORS
from app.config import ALLWED_ORIGINS
from app.models import RentRequest, HouseRequest, CondoRequest,SimulationResponse, YearRow
from .services.simulation import simulate_rent, simulate_house, simulate_condo
from app.services.simulation import simulate_rent,simulate_house, simulate_condo
from pydantic import ValidationError

app = Flask(__name__)
CORS(app, origins=ALLWED_ORIGINS, supports_credentials=True)

def to_response(mode: str, region: str, years: int, rows_dict):
    rows = [YearRow(**r).dict() for r in rows_dict]
    return SimulationResponse(mode=mode, region=region, years=years, rows=rows).dict()

@app.route('/simulate/rent', methods=['POST'])
def rent_api():
    try:
        payload = request.get_json(force=True)
        req = RentRequest(**payload)
        rows = simulate_rent(req)
        return jsonify(to_response("rent", req.region, req.horizon_years, rows))
    except ValidationError as e:
        return jsonify({"error": "validation_error", "detail": e.errors()}), 400

@app.route('/simulate/house', methods=['POST'])
def house_api():
    try:
        payload = request.get_json(force=True)
        req = HouseRequest(**payload)
        rows = simulate_house(req)
    except ValidationError as e:
        return jsonify({"error": "validation_error", "detail": e.errors()})

@app.route('/simulate/condo', methods=['POST'])
def condo_api():
    try:
        payload = request.get.json(force=True)
        req = CondoRequest(**payload)
        rows = simulate_condo(req)
        return jsonify(to_response("condo", req.region, req.horizon_years, rows))
    except ValidationError as e:
        return jsonify({"error": "validation_error", "detail": e.errors()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

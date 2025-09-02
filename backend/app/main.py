from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import ValidationError
from app.models import (RentRequest, HouseRequest, CondoRequest, SimulationResponse, YearRow)
from app.services.simulation import simulate_rent, simulate_house, simulate_condo
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
CORS(
    app,
    resources={r"/simulate/*": {"origins": ["http://localhost:5173"]}},
    supports_credentials=False,
    allow_headers=["Content-Type"],
    methods=["POST", "OPTIONS", "GET"],
)

def to_response(mode: str, years: int, rows_dict, region=None):
    rows = [YearRow(**r).dict() for r in rows_dict]
    return SimulationResponse(mode=mode, region=region, years=years, rows=rows).dict()

@app.route("/ping", methods=["GET"])
def ping():
    return "pong"

@app.errorhandler(HTTPException)
def on_http_error(e):
    return jsonify({"error": e.name, "message": e.description}), e.code

@app.route("/simulate/rent", methods=["POST"])
def rent_api():
    try:
        payload = request.get_json(force=True)
        req = RentRequest(**payload)
        rows = simulate_rent(req)
        return jsonify(to_response("rent", req.horizon_years, rows))
    except ValidationError as e:
        return jsonify({"error": "validation_error", "detail": e.errors()}), 400

@app.route("/simulate/house", methods=["POST"])
def house_api():
    try:
        payload = request.get_json(force=True)
        req = HouseRequest(**payload)
        rows = simulate_house(req)
        return jsonify(to_response("house", req.horizon_years, rows, region=req.region))
    except ValidationError as e:
        return jsonify({"error": "validation_error", "detail": e.errors()}), 400

@app.route("/simulate/owner", methods=["POST", "OPTIONS"])
def owner_api():
    if request.method == "OPTIONS":
        return ("", 204)
    try:
        payload = request.get_json(force=True)
        req = HouseRequest(**payload)
        rows = simulate_house(req)
        return jsonify(to_response("house", req.horizon_years, rows, region=req.region))
    except ValidationError as e:
        return jsonify({"error": "validation_error", "detail": e.errors()}), 400

@app.route("/simulate/condo", methods=["POST"])
def condo_api():
    try:
        payload = request.get_json(force=True)
        req = CondoRequest(**payload)
        rows = simulate_condo(req)
        return jsonify(to_response("condo", req.horizon_years, rows, region=req.region))
    except ValidationError as e:
        return jsonify({"error": "validation_error", "detail": e.errors()}), 400

# ★ デバッグ用: 例外を JSON で返す（フロント側の「CORSっぽく見える500」の正体がわかる）
@app.errorhandler(Exception)
def on_exception(e):
    import traceback
    return jsonify({
        "error": "server_error",
        "message": str(e),
        "trace": traceback.format_exc()
    }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
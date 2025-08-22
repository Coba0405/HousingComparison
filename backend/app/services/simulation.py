# rent/house/condo の「月次イベントの載せ方」だけを分岐して他は共通化
from .loan import monthly_payment
from .taxes import tax_rate

def simulate_rent(req):
    months = req.horizon_years * 12
    rows_by_year = {}
    cum = 0

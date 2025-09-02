# rent/house/condo の「月次イベントの載せ方」だけを分岐して他は共通化
from .loan import monthly_payment
from .taxes import tax_rate

def simulate_rent(req):
    months = req.horizon_years * 12
    rows_by_year = {}
    cum = 0
    for m in range(months):
        y = m // 12 + 1
        rent = req.rent_monthly
        renewal = (1 if (m + 1) % (req.renewal_interval_years * 12) == 0 else 0) * req.renewal_fee_amount
        contents = (1 if (m + 1) % (req.contents_insurance_interval_years * 12) == 0 else 0) * req.contents_insurance_amount
        total = rent + renewal + contents
        acc = rows_by_year.setdefault(y, dict(rent=0, renewal=0, contents=0, total=0))
        acc["rent"] += rent; acc["renewal"] += renewal; acc["contents"] += contents; acc["total"] += total
    rows, cum_out = [], 0
    for y in range(1, req.horizon_years + 1):
        r = rows_by_year.get(y, dict(rent=0, renewal=0, contents=0, total=0))
        cum_out += r["total"]
        rows.append(dict(
            year=y, rent=round(r["rent"]), renewal_fee=round(r["renewal"]), contents_insurance=round(r["contents"]),
            loan_payment=0, fire_insurance=0, property_taxes=0, house_renovation=0, mgmt_fee=0, reserve_fee=0,
            total_cost_year=round(r["total"]), cum_total_cost=round(cum_out)
        ))
    return rows

def simulate_house(req):
    months = req.horizon_years * 12
    mpay = monthly_payment(req.home_price, req.loan_annual_rate, req.loan_years)
    rate = tax_rate(req.region)
    annual_tax = req.home_price * rate
    rows_by_year, cum_out = {}, 0
    for m in range(months):
        y = m // 12 + 1
        month_in_year = m % 12 + 1
        loan = mpay
        fire = req.fire_insurance_monthly
        taxes = annual_tax if month_in_year == req.property_tax_charge_month else 0
        # 10年ごと + 指定月
        renov = req.house_renovation_every_10y_amount if ((m + 1) % (10 * 12) == 0 and month_in_year == req.house_renovation_change_month) else 0
        total = loan + fire + taxes + renov
        acc = rows_by_year.setdefault(y, dict(loan=0, fire=0, taxes=0, renov=0, total=0))
        acc["loan"] += loan; acc["fire"] += fire; acc["taxes"] += taxes; acc["renov"] += renov; acc["total"] += total
    rows = []
    for y in range(1, req.horizon_years + 1):
        r = rows_by_year.get(y, dict(loan=0, fire=0, taxes=0, renov=0, total=0))
        cum_out += r["total"]
        rows.append(dict(
            year=y,
            rent=0, renewal_fee=0, contents_insurance=0,
            loan_payment=round(r["loan"]), fire_insurance=round(r["fire"]), property_taxes=round(r["taxes"]),
            house_renovation=round(r["renov"]), mgmt_fee=0, reserve_fee=0,
            total_cost_year=round(r["total"]), cum_total_cost=round(cum_out)
        ))
    return rows

def stepped_value(month_index, base, step_years, step_pct):
    if base == 0 or step_pct == 0: return base
    step = (month_index // (step_years * 12))
    return round(base * ((1 + step_pct) ** step))

def simulate_condo(req):
    months = req.horizon_years * 12
    mpay = monthly_payment(req.home_price, req.loan_annual_rate, req.loan_years)
    rate = tax_rate(req.region)
    annual_tax = req.home_price * rate
    rows_by_year, cum_out = {}, 0
    for m in range(months):
        y = m // 12 + 1
        month_in_year = m % 12 + 1
        loan = mpay
        fire = req.fire_insurance_monthly
        taxes = annual_tax if month_in_year == req.property_tax_charge_month else 0
        mgmt = stepped_value(m, req.mgmt_monthly0, 5, req.mgmt_increase_every_5y_pct)
        reserve = stepped_value(m, req.reserve_monthly0, 5, req.reserve_increase_every_5y_pct)
        total = loan + fire + taxes + mgmt + reserve
        acc = rows_by_year.setdefault(y, dict(loan=0, fire=0, taxes=0, mgmt=0, reserve=0, total=0))
        acc["loan"] += loan; acc["fire"] += fire; acc["taxes"] += taxes; acc["mgmt"] += mgmt; acc["reserve"] += reserve; acc["total"] += total
    rows = []
    for y in range(1, req.horizon_years + 1):
        r = rows_by_year.get(y, dict(loan=0, fire=0, taxes=0, mgmt=0, reserve=0, total=0))
        cum_out += r["total"]
        rows.append(dict(
            year=y, rent=0, renewal_fee=0, contents_insurance=0,
            loan_payment=round(r["loan"]), fire_insurance=round(r["fire"]), property_taxes=round(r["taxes"]),
            house_renovation=0, mgmt_fee=round(r["mgmt"]), reserve_fee=round(r["reserve"]),
            total_cost_year=round(r["total"]), cum_total_cost=round(cum_out)
        ))
    return rows

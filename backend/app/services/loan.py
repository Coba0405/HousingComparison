def monthly_payment(principal: float, annual_rate: float, years: int) -> float:
    n = years * 12
    if annual_rate == 0:
        return principal / n
    r = annual_rate / 12
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)

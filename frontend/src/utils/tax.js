export function calcKotos(tokeiRate, landAreaSqm, rosenkaPerSqm) {
  const valuation = rosenkaPerSqm * 0.875 * landAreaSqm;

  const smallArea = Math.min(landAreaSqm, 200);
  const largeArea = Math.max(landAreaSqm - 200, 0);
  const smallVal = valuation * (smallArea / (landAreaSqm || 1));
  const largeVal = valuation * (largeArea / (landAreaSqm || 1));

  const kazeiKotei = smallVal / 6 + largeVal / 3;        // 固定資産税の課税標準
  const fixedTax = kazeiKotei * 0.014;                    // 1.4%

  const kazeiTokei = smallVal / 3 + (largeVal * 2) / 3;   // 都市計画税の課税標準
  const cityPlanningTax = kazeiTokei * tokeiRate;

  return {
    valuation: Math.round(valuation),
    fixed_tax: Math.round(fixedTax),
    city_planning_tax: Math.round(cityPlanningTax),
    total: Math.round(fixedTax + cityPlanningTax),
  };
}

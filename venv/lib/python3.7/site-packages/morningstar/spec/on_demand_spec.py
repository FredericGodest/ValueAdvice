from enum import Enum


class OnDemandReturnType(Enum):
    """ Morningstar Return Types in OnDemand

    Morningstar On Demand Webportal Dictionary - Return Types
    """
    TotalReturn = "1"
    LoadAdjustedReturn = "2"
    SECPreLiquidationReturn = "3"
    SECPostLiquidationReturn = "4"
    TaxCostRatioReturn_PreLiquidation = "5"
    MarketReturn = "6"
    IncomeReturn_PreTax = "7"
    CapitalGainReturn = "8"
    PremiumDiscountReturn = "9"
    IndexReturn = "10"
    TaxableEquivalentReturn = "11"
    NonStandardized_LoadAdjustedReturn = "12"
    GrossManagementFeeReturn = "13"
    SECPreLiquidationReturn_MarketPrice = "14"
    SECPostLiquidationReturn_MarketPrice = "15"
    TaxCostRatioReturn_PreLiquidation_MarketPrice = "16"
    PriceReturn = "17"
    TaxAdjustedReturn = "18"
    ExchangeRateReturn = "19"
    InvestorReturn = "20"
    NonAuditedReturn = "21"
    PreliminaryReturn = "31"
    EPRTotalReturn = "101"
    EPRLoadAdjustedReturn = "102"
    EPRNonStandardizedLoadAdjustedReturn = "112"
    PreInceptionTotalReturn = "201"
    PreInceptionLoadAdjustedReturn = "202"
    PreInceptionNASDNonStandardizedReturn = "212"
    SurvivorshipBiasFreeReturn = "301"
    TaxCostRatioReturn_PostLiquidation = "25"
    SECStandardizedReturn = "22"
    TaxAndLoadAdjustedReturn = "23"
    TaxAdjustedIncomeReturn = "27"
    
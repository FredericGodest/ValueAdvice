class RIPS:
    __slots__ = ('SecId', 'PerformanceId', 'Date', 'Deleted', 'Unit_BAS', 'Unit_USD', 'Unit_EUR', 'Unit_GBP',
                 'Unit_CHF', 'Unit_DKK', 'Unit_NOK', 'Unit_SEK', 'Unit_JPY', 'LastUpdate', 'Unit_SGD',
                 'ReturnType', 'Filled', 'Unit_TWD', 'Unit_HKD', 'Unit_MYR', 'Unit_CNY', 'Unit_ILS', 'Unit_INR',
                 'Unit_CAD', 'Unit_KWD', 'Unit_PLN', 'Unit_AUD', 'Unit_THB', 'Unit_KRW', 'Unit_NZD')

    @classmethod
    def from_dict(cls, row: dict):
        obj = cls()
        for k, v in row.items():
            setattr(obj, k, v)
        return obj

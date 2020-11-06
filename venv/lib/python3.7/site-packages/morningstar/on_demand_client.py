from morningstar.provider.on_demand import OnDemand
from morningstar.config import config
from morningstar.models.rips import RIPS
from morningstar.spec.on_demand_spec import OnDemandReturnType
from lxml import etree
from typing import Optional


class OnDemandClient():
    xpath_share_performanceid_basecurrency = "/FundShareClass/PerformanceId/Result[./IsBaseCurrency = 'true']/PerformanceId/text()"
    xpath_universe_morningstarid = "/FundShareClassList/ShareClass/Id/text()"

    def __init__(self, provider=None):
        """ Wraps Provider

        Args:
            provider (Provider): provider instance
        """
        if provider is None:
            provider = OnDemand(config=config.get('provider')['ondemand'])
        self.provider = provider

    def login(self):
        """
        Establish a session before using any method of provider
        """
        self.provider.login()

    def get_historical_rips_by_performanceid(self,
                                             performance_id: str,
                                             return_type: OnDemandReturnType,
                                             start_date: str = '',
                                             end_date: str = '') -> [RIPS]:
        """Fetches historical RIPS for the given performance id

            Args:
                performance_id (str): e.g. "0P0000OO1Z"
                return_type (OnDemandReturnType): e.g. TotalReturn
                start_date (str): "%Y-%m-%d"
                end_date (str): "%Y-%m-%d"

            Returns:
                List of RIPS objects, one for each date
        """

        # Download csv data associated with this performance id
        params_historydata = {'ClientId': self.provider.config['clientid'],
                              'DataType': 'rips',
                              'StartDate': start_date,
                              'EndDate': end_date,
                              'PriceTypeId': str(return_type.value),
                              'PerformanceId': performance_id}
        return self.provider.history_data(params=params_historydata)

    def get_historical_rips_by_fundshareclassid(self,
                                                fundshareclass_id: str,
                                                return_type: OnDemandReturnType,
                                                start_date: str = '',
                                                end_date: str = '') -> [RIPS]:
        """Fetches historical RIPS for the fundshare with the given fundshareclass_id using 
            the performance id associated with its base currency

            Note: 
                If no or more than 1 performance id in base currency is found, a ValueError is raised. 

            Args:
                fundshareclass_id (str): e.g. "F00000IRY4"
                return_type (OnDemandReturnType): e.g. TotalReturn
                start_date (str): "%Y-%m-%d"
                end_date (str): "%Y-%m-%d"

            Returns:
                List of RIPS objects, one for each date
        """

        # Use the fundshareclass_id to retrieve the share's xml
        params_sharexml = {'Package': 'EDW', 'IDType': 'FundShareClassId',
                           'ClientId': self.provider.config['clientid'],
                           'Id': fundshareclass_id}

        root_n_share = self.provider.data_output(params=params_sharexml)

        # Read out basecurrency's performance id
        share_performanceid_basecurrency = root_n_share.xpath(
            self.xpath_share_performanceid_basecurrency)
        if len(share_performanceid_basecurrency) == 0:
            raise ValueError("No performance id in basecurrency could be found")
        if len(share_performanceid_basecurrency) > 1:
            raise ValueError(
                "More than 1 performance id in basecurrency was found: " + str(share_performanceid_basecurrency))
        share_performanceid_basecurrency = str(
            share_performanceid_basecurrency[0])

        # Retrieve RIPS using performance id
        return self.get_historical_rips_by_performanceid(performance_id=share_performanceid_basecurrency,
                                                         return_type=return_type,
                                                         start_date=start_date,
                                                         end_date=end_date)

    def get_historical_rips_by_isin(self,
                                    isin: str,
                                    return_type: OnDemandReturnType,
                                    start_date: str = '',
                                    end_date: str = '',
                                    universe: str = '') -> [RIPS]:
        """Fetches historical RIPS for the fundshare with the given ISIN using the performance id in basecurrency

            Note:
                The ISIN is searched in the specified universe to obtain the morningstar id. From the morningstar id,
                the performance id associated with the base currency is used to retrieve the RIPS.
                If the share is obsolete for too long (45d), or not found in the given universe, or if no
                performance id in base currency can be found, a ValueError is raised. 

            Args:
                isin (str): e.g. "IE00B5BMR087"
                return_type (OnDemandReturnType): e.g. TotalReturn
                start_date (str): "%Y-%m-%d"
                end_date (str): "%Y-%m-%d"
                universe (str): e.g. "CHE"

            Returns:
                List of RIPS objects, one for each date
            """

        # Get universe to find Morningstar Id corresponding to isin
        #   no start and end date for search of isin in universe, max length
        data_get_fundshare_universe = {'ClientId': self.provider.config['clientid'],
                                       'ActiveStatus': '',  # obsolete and active, max coverage (last 45d)
                                       'InvestorType': '',  # both, dont care as only to get id
                                       'LegalStructureId': '',  # all types of funds
                                       'ISIN': isin,
                                       'CountryId': universe}
        root_n_universe = self.provider.get_universe(params=data_get_fundshare_universe)

        # read out ms id from universe xml
        #   It is unfortunately possible that a search by ISIN results in the correct fundshare which has
        #   a different ISIN than the one used for searching. In the resulting universe xml, it is also only
        #   listed with this other ISIN and hence cannot be found by subsetting in the xpath with the searched ISIN.
        #   (ie by using [./ISIN = '"+isin+"'] in xpath). Therefore, because only a single share 
        #   should be found, read out directly without searching by ISIN in the xml
        ms_id = root_n_universe.xpath(self.xpath_universe_morningstarid)
        if len(ms_id) == 0:
            raise ValueError(
                'No Morningstar Id could be found for ISIN {}. Maybe the share is dead for too long or in a different universe?'.format(
                    isin))
        if len(ms_id) > 1:
            raise ValueError('More than one Morningstar Id found for ISIN {}.'.format(isin))
        ms_id = str(ms_id[0])

        # Use the Morningstar Id to retrieve the RIPS of the basecurrency
        return self.get_historical_rips_by_fundshareclassid(fundshareclass_id=ms_id,
                                                            return_type=return_type,
                                                            start_date=start_date,
                                                            end_date=end_date)

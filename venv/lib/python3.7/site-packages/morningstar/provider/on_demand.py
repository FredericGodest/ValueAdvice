import codecs
import csv

import requests
from lxml import etree

from morningstar.models.rips import RIPS
from morningstar.provider.provider import Provider


class OnDemand(Provider):
    """OnDemand API

    Note:
        This class combines multiple endpoints:
            - https://edw.morningstar.com/login.aspx
            - https://edw.morningstar.com/Logout.aspx
            - https://edw.morningstar.com/GetUniverseXML.aspx
            - https://edw.morningstar.com/DataOutput.aspx
            - https://edw.morningstar.com/HistoryData/HistoryData.aspx

        Login needs to be called before using any of the other functions
        If logout is called, all clients currently accessing the API are logged out

    Attributes:
        credentials (dict): Provider specific configuration including "username" and "password"
    """

    url_login = "https://edw.morningstar.com/login.aspx"
    url_logout = "https://edw.morningstar.com/Logout.aspx"
    url_getuniverse = "https://edw.morningstar.com/GetUniverseXML.aspx"
    url_dataoutput = "https://edw.morningstar.com/DataOutput.aspx"
    url_historydata = "https://edw.morningstar.com/HistoryData/HistoryData.aspx"

    def __init__(self, config):
        super().__init__(config)
        self.session = None

    def login(self):
        self.session = requests.Session()
        ms_data_login = {
            'email': self.config['username'], 'password': self.config['password']}
        self.session.post(self.url_login, data=ms_data_login)

    def logout(self):
        self._assert_login()
        ms_data_logout = {'clientid': self.config['clientid']}
        self.session.post(url=self.url_logout, data=ms_data_logout)

    def _xml_from_url(self, url: str, params: dict):
        self._assert_login()
        r_url = self.session.get(url, params=params)
        return etree.fromstring(r_url.content)

    def get_universe(self, params: dict) -> [etree]:
        return self._xml_from_url(url=self.url_getuniverse, params=params)

    def data_output(self, params: dict) -> [etree]:
        return self._xml_from_url(url=self.url_dataoutput, params=params)

    def history_data(self, params: dict) -> [RIPS]:
        self._assert_login()
        with self.session.get(self.url_historydata, params=params) as r_download_csv:
            # read rows as dict to convert to rips class
            cr = csv.DictReader(codecs.iterdecode(
                r_download_csv.iter_lines(), 'utf-8'), delimiter=';')
            return [RIPS.from_dict(row_dict) for row_dict in cr]

    def _assert_login(self):
        if self.session is None:
            raise ValueError("A session has to be established first by calling login()")
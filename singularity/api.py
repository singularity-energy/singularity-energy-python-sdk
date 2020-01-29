from enum import Enum
from json import JSONDecodeError

import requests as req

from .exceptions import APIException, GatewayTimeoutException


def _handle_error(error_res):
    if error_res.headers.get('Content-Type') != 'application/json':
        raise Exception
    else:
        json_res = error_res.json()
        if error_res.status_code <= 500 and 'error_code' in json_res:
            raise APIException(
                json_res.get('error_code'),
                json_res.get('error_message'),
                error_res.status_code
            )
        elif 'detail' in json_res:
            raise APIException(
                None,
                json_res.get('detail'),
                error_res.status_code
            )
        else:
            raise APIException(None, None, error_res.status_code)


class Regions(Enum):
    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    ISONE = 'ISONE'
    NYISO = 'NYISO'
    CAISO = 'CAISO'
    MISO = 'MISO'
    IESO = 'IESO'
    PJM = 'PJM'


class SingularityAPI(object):
    BASE_URL = 'https://api.singularity.energy'


    def __init__(self, api_key):
        self.api_key = api_key


    def _get_headers(self):
        return {
            'X-Api-Key': self.api_key,
        }


    def _format_search_url(self, region, event_type, start, end, postal_code, filter_):
        if region is None and postal_code is not None:
            url = '{}/v1/region_events/search?postal_code={}&start={}&end={}&event_type={}'\
                .format(
                    self.BASE_URL,
                    postal_code,
                    start,
                    end,
                    event_type
                )
            if filter_ is not None:
                url += '&filter={}'.format(filter_)
            return url
        else:
            url = '{}/v1/region_events/search?region={}&start={}&end={}&event_type={}'\
                .format(
                    self.BASE_URL,
                    region.name,
                    start,
                    end,
                    event_type
                )
            if filter_ is not None:
                url += '&filter={}'.format(filter_)
            return url


    def _format_find_url(self, dedup_key):
        return '{}/v1/region_events/{}'.format(
            self.BASE_URL,
            dedup_key
        )


    def find_region_event(self, dedup_key, raise_=True):
        """Find an event by its dedup key.

        :dedup_key string: the deduplication key for the event
        :raise optional boolean: (default: True) whether to raise or not on a
            bad response code
        :returns: a single region event or None if not found and
            we're told not to raise an exception
        :raises: Exception if there is a bad response code
        """
        url = self._format_find_url(dedup_key)
        res = req.get(url, headers=self._get_headers())
        if res.status_code == 200:
            return res.json()['data']
        elif raise_:
            _handle_error(res)


    def find_all_region_events(self, dedup_keys, raise_=False):
        """Find all events with the given dedup keys.

        :dedup_keys list[string]: the list of dedup keys to check
            for existence
        """
        url = self.BASE_URL + '/v1/region_events/bulk-find'
        res = req.post(url, headers=self._get_headers(), json={'dedup_keys': dedup_keys})
        if res.status_code == 200:
            return res.json()['data']
        elif raise_:
            _handle_error(res)


    def search_region_events_for_postal_code(self, postal_code, event_type, start, end, filter_=None):
        """Search for region events by a postal code instead of a region.

        :postal_code string: a postal code to use for the search
        :event_type string: an event type to search for
        :start string: an iso8601 datetime string with a timezone
        :end string: an iso8601 datetime string with a timezone
        :filter string: a string in the format key:value to filter the events for
        :returns: an array of data
        :raises: APIException if there is a bad response code
        """
        url = self._format_search_url(None, event_type, start, end, postal_code=postal_code, filter_=filter_)
        res = req.get(url, headers=self._get_headers())
        if res.status_code == 200:
            return res.json()['data']
        else:
            _handle_error(res)


    def search_region_events(self, region, event_type, start, end, filter_=None):
        """Search for region events over a period of time.

        :region Regions: a region from the Regions enum
        :event_type string: an event type to search for
        :start string: an iso8601 datetime string with a timezone
        :end string: an iso8601 datetime string with a timezone
        :filter string: a string in the format key:value to filter the events for
        :returns: an array of data
        :raises: APIException if there is a bad response code
        """
        url = self._format_search_url(region, event_type, start, end, None, filter_)
        res = req.get(url, headers=self._get_headers())
        if res.status_code == 200:
            return res.json()['data']
        else:
            _handle_error(res)


    def get_all_emission_factors(self):
        """Fetch all the emission factors available in the emissions API.

        :returns list: a list of all supported emission factor sources and their values
        """
        url = self.BASE_URL + '/v1/emissions/all-factors'
        res = req.get(url, headers=self._get_headers())
        if res.status_code == 200:
            return res.json()['data']['generated_intensity']
        else:
            _handle_error(res)


    def calculate_generated_carbon_intensity(self, genfuelmix, region, source='EGRID_2016'):
        """Calculate the intensity for a given genfuelmix

        :genfuelmix dict: the 'data' part of a 'generated_fuel_mix' event
        :region Regions: a region from the Regions enum
        :source string: (default: EGRID_2016) a string representing the source data to use
            for the emission factors
        :returns: the rate of carbon emissions for a genfuelmix in lbs/MWh
        """
        url = self.BASE_URL + '/v1/emissions/calculate-intensity/generated'
        payload = {
            'genfuelmix': genfuelmix,
            'region': region.name,
            'source': source,
        }
        res = req.post(url, headers=self._get_headers(), json=payload)
        if res.status_code == 200:
            return res.json()['data']['generated_intensity']
        else:
            _handle_error(res)


    def calculate_marginal_carbon_intensity(self, fuelmix_percents, region, source='EGRID_2016'):
        """Calculate the intensity for a given fuelmix percentage

        :fuelmix_percents dict: the 'data' part of a 'marginal_fuel_mix' event
        :region Regions: a region from the Regions enum
        :source string: (default: EGRID_2016) a string representing the source data to use
            for the emission factors
        :returns: the rate of carbon emissions for a fuelmix in lbs/MWh
        """
        url = self.BASE_URL + '/v1/emissions/calculate-intensity/marginal'
        payload = {
            'fuelmix_percents': fuelmix_percents,
            'region': region.name,
            'source': source,
        }
        res = req.post(url, headers=self._get_headers(), json=payload)
        if res.status_code == 200:
            return res.json()['data']['marginal_intensity']
        else:
            _handle_error(res)


    def latest_region_events(self, region_or_postal_code, event_type='carbon_intensity'):
        """Get the latest region events for a region or postal code.

        :region_or_postal_code Region|string: the region or postal code to query
        :event_type string (default: carbon_intensity): the event type to query for
            currently only carbon_intensity and generated_fuel_mix are supported
        :returns: a dict of the latest event and forecasts for the event
        """

        url = self.BASE_URL + '/v1/region_events/{}/latest?event_type={}'.format(region_or_postal_code, event_type)
        res = req.get(url, headers=self._get_headers())
        if res.status_code == 200:
            return res.json()['data']
        else:
            _handle_error(res)
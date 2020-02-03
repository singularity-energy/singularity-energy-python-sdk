from enum import Enum
from json import JSONDecodeError

import requests as req

from .__version__ import __version__
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
    """The Singularity API is available through api.singularity.energy.

    Details on the specific HTTP endpoints can be found in the `API's official
    documentation <https://docs.google.com/document/d/1tUS6DMy1XzCdprJ5LMDXeXH4EzaFhPLbgX-9BuE9l_0/edit?usp=sharing>`_.

    All API calls are done with once (no retry logic) and are sent with an X-Api-Key header and a User-Agent header.
    """

    BASE_URL = 'https://api.singularity.energy'


    def __init__(self, api_key):
        self.api_key = api_key


    def _get_headers(self):
        return {
            'X-Api-Key': self.api_key,
            'User-Agent': 'Python/Singularity SDK v{}'.format(__version__)
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
                    str(region),
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


    def find_region_event(self, dedup_key):
        """Find an event by its dedup key.

        Any region event will have a dedup_key as a top level field::

            from datetime import datetime as dt, timedelta as td
            from singularity import SingularityAPI, Regions

            singularity = SingularityAPI('API_KEY')
            nowstring = dt.utcnow().isoformat() + 'Z'
            before = (dt.utcnow() - td(minutes=10)).isoformat() + 'Z'
            events = singularity.search_region_events(
                Regions.ISONE,
                'generated_fuel_mix',
                before,
                nowstring
            )
            # get the dedup_key from the event
            key = events[0]['dedup_key']

        :param dedup_key: the deduplication key for the event
        :returns: a single region event or None if not found and
            we're told not to raise an exception
        :raises: APIException if there is a bad response code, e.g. 404
        """
        url = self._format_find_url(dedup_key)
        res = req.get(url, headers=self._get_headers())
        if res.status_code == 200:
            return res.json()['data']
        else:
            _handle_error(res)


    def find_all_region_events(self, dedup_keys):
        """Find all events with the given dedup keys.

        :param dedup_keys: the list of dedup keys to check
            for existence
        :returns: a list of events found by the provided keys
        :raises: APIException if any events are not found
        """
        url = self.BASE_URL + '/v1/region_events/bulk-find'
        res = req.post(url, headers=self._get_headers(), json={'dedup_keys': dedup_keys})
        if res.status_code == 200:
            return res.json()['data']
        else:
            _handle_error(res)


    def search_region_events_for_postal_code(self, postal_code, event_type, start, end, filter_=None):
        """Search for region events by a postal code instead of a region.

        Currently only ISONE, NYISO, and PJM have mappings from postal code <> ISO region. Any postal codes
        from any other region, for example, California, will not be found.

        :param postal_code: a string of a postal code to use for the search, e.g. 02139
        :param event_type: a string of the event type to search for
        :param start: an iso8601 datetime string with a timezone
        :param end: an iso8601 datetime string with a timezone
        :param filter_: (optional) a string in the format key:value to filter the events for
        :returns: an array of data region events
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

        Currently, the supported regions are:
         - ISONE
         - NYISO
         - PJM
         - IESO
         - CAISO
         - MISO

        Regions are updated often so check back soon if you want to use one that isn't listed.

        The :ref:`region events <Event Types>` that are currently supported can be found in the notes section of the documentation.

        Usage::

            from singularity import SingularityAPI, Regions
            s = SingularityAPI('API_KEY')
            region_string = 'PJM'
            region = Regions(region_string)  # or you can use Regions.PJM
            s.search_region_events(region, 'carbon_intensity', '2020-01-20T00:00:00Z', '2020-01-21T00:00:00Z')


        :param region: a region from the Regions enum
        :param event_type: an event type to search for
        :param start: an iso8601 datetime string with a timezone
        :param end: an iso8601 datetime string with a timezone
        :param filter: a string in the format key:value to filter the events for.
            a filter either looks in `meta` or `data` objects. Filters must be
            in the format of `data.some_key:some_value`
        :returns: an array of region events
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
            return res.json()
        else:
            _handle_error(res)


    def calculate_generated_carbon_intensity(self, genfuelmix, region, source='EGRID_2016'):
        """Calculate the intensity for a given genfuelmix.

        The generated rate is calculated by multiplying the generated MW for each fuel type
        by its emission factor for the given source. You can find all sources listed from a call
        to the `get_all_emission_factors` function. Each object in the returned list will
        have an `id` which can be passed as the `source` parameter to this function.

        :param genfuelmix: the `data` part of a `generated_fuel_mix` event
        :param region: a region from the Regions enum
        :param source: (default: EGRID_2016) a string representing the source data to use
            for the emission factors.
        :returns: the rate of carbon emissions for a genfuelmix in lbs/MWh
        :raises: an APIException if a bad response code is returned
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

        :param fuelmix_percents: the `data` part of a `marginal_fuel_mix` event
        :param region: a region from the Regions enum
        :param source: (default: EGRID_2016) a string representing the source data to use
            for the emission factors
        :returns: the rate of carbon emissions for a fuelmix in lbs/MWh
        :raises: an APIException if a bad response code is returned
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

        :param region_or_postal_code: the region or postal code to query. Either a region from
            the Regions enum or a string of a postal code
        :param event_type: (default: carbon_intensity) the event type to query for
            currently only carbon_intensity and generated_fuel_mix are supported
        :returns: a dict of the latest event and forecasts for the event
        :raises: an APIException if a bad response code is returned
        """

        url = self.BASE_URL + '/v1/region_events/{}/latest?event_type={}'.format(region_or_postal_code, event_type)
        res = req.get(url, headers=self._get_headers())
        if res.status_code == 200:
            return res.json()['data']
        else:
            _handle_error(res)

    def carbon_flow_by_region(self, datestring, regions=['ISONE', 'NYISO', 'PJM', 'IESO']):
        """Get the region_flow and carbon_intensity for the listed regions.

        :param datestring: the ISO8601 string to use to find all the events
        :param regions: (default: ['ISONE', 'NYISO', 'PJM', 'IESO']) a list of strings as
            the regions to search for
        :returns: a dict of region codes -> carbon_intensity, region_flow & generated_fuel_mix
            events for the timestamp
        """
        gathered = {}

        for region in regions:
            ci_event = self.search_region_events(Regions(region), 'carbon_intensity', datestring, datestring)
            region_flow_event = self.search_region_events(Regions(region), 'region_flow', datestring, datestring)
            gfm_event = self.search_region_events(Regions(region), 'generated_fuel_mix', datestring, datestring)
            gathered[region] = {
                'carbon_intensity': ci_event[0] if 0 < len(ci_event) else None,
                'region_flow': region_flow_event[0] if 0 < len(region_flow_event) else None,
                'generated_fuel_mix': gfm_event[0] if 0 < len(gfm_event) else None,
            }

        return gathered
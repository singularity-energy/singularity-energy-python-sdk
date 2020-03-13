Exceptions
================

Possible exceptions that could be raised by the SingularityAPI class

.. module:: singularity

.. autoclass:: APIException
   :members:
   :inherited-members:

.. autoclass:: GatewayTimeoutException
   :members:
   :inherited-members:


Handling Exceptions
^^^^^^^^^^^^^^^^^^^

When using SingularityAPI, you may encounter times when you get a bad response.
If this is the case, the response will be wrapped in an Exception object for you.
Known exceptions will wither be a `GatewayTimeoutException` or `APIException`.
Here is an example of catching them::

    from singularity import SingularityAPI, APIException, Regions, GatewayTimeoutException

    singularity = SingularityAPI('API_KEY')
    e = None
    try:
        singularity.search_region_events(
            Regions.ISONE,
            'generated_fuel_mix',
            '2020-01-02T00:00:00Z',
            '2020-01-03T00:00:00Z',
            filter_='natural_gas_marginal:1.0'
        )
    except GatewayTimeoutException:
        # feel free to retry
    except APIException as exc:
        e = exc

    e

Putting that code into your python REPL will give you an error and inspecting the error will show you::

    <APIException[400] (bad-search-filter: "filter" can only apply to data or meta fields (prefix your filer with data. or meta.))>

In the event that you catch a GatewayTimeoutException, you should feel free to retry the request as many times as you'd like
until you get a successful response from the API or until you catch an APIException.
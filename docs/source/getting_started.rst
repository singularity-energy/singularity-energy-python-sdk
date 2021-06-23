Getting Started
=================

Before you can start using Singularity's API, you need to have an API key.

To get an API key, you can reach out to Jeff Burka (jeffrey.burka@singularity.energy) and ask for one.

Once you have an API key, you can use the python SDK::

    from singularity import SingularityAPI, Regions
    s_api = SingularityAPI('API_KEY')

    # get the latest region events for the ISONE region
    s_api.latest_region_events(Regions.ISONE)

    # use Singularity's (incomplete) zip code lookup to find
    # events for a zip code
    s_api.latest_region_events('02139')

Singularity's API comes with a variety of requests you can make. To see more documentation on them :ref:`check out the API documentation<Singularity API>`
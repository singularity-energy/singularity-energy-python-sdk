Event Types
=============

The Singularity API currently offers lots of different region events, though it doesn't offer
great discoverability of the event types solely via the API. On this page you can learn about
many of the differen types of region events and how to interpret them.



Fuel Mix
^^^^^^^^^^^^^^^^^^^
All BAs listed in the :ref:`Regions` page have generated fuel mix (genfuelmix) events. Genfuelmix events
are scraped directly from the BA and expanded to fit five minute windows. There are three different event
types that represent genfuelmix events:

 - raw.generated_fuel_mix: these events are not normalized to fit a 5-minute window and often the labels 
   in `data` are unchanged from the raw source of the event
 - raw.marginal_fuel_mix: these events are listed for regions that expose their marginal_fuel_mix data. Most regions
   do not expose this data.
 - generated_fuel_mix: these events are normalized to fit a 5-minute window and the labels have all been
   standardized across different regions. The only exception is ISONE, which includes the marginal flag
   for to note the fuels used when demand exceeds the forecast.
 - marginal_fuel_mix: these events are either normalized from the data provided by the ISO or estimated by
   Singularity.
 - forecast.generated_fuel_mix: these events are created based on a generated_fuel_mix event. Each
   generated_fuel_mix event will create between 12 and 24 different forecasts (from 5 minutes out to
   120 minutes out) and the forecast horizon is denoted in the `data` as the field
   `forecast_horizon_in_minutes`


Here are three example events::

    forecast_genfuelmix = {'data': {'coal_marginal': 0.0,
      'coal_mw': 428.5593551913782,
      'forecast_horizon_in_minutes': 5,
      'hydro_marginal': 0.0,
      'hydro_mw': 1164.4898876044863,
      'landfill_gas_marginal': 0.0,
      'landfill_gas_mw': 29.00961528281686,
      'natural_gas_marginal': 1.0,
      'natural_gas_mw': 5313.924400637518,
      'nuclear_marginal': 0.0,
      'nuclear_mw': 3352.0121387202903,
      'other_marginal': 0.0,
      'other_mw': 3.9986099517174827,
      'refuse_marginal': 0.0,
      'refuse_mw': 363.60369003994896,
      'solar_marginal': 0.0,
      'solar_mw': 14.645047471485709,
      'wind_marginal': 0.0,
      'wind_mw': 694.3169889141071,
      'wood_marginal': 0.0,
      'wood_mw': 243.5974269480731},
    'dedup_key': 'forecast.generated_fuel_mix:ISONE:5I:2020-02-03T16:30:00-05:00',
    'event_type': 'forecast.generated_fuel_mix',
    'region': 'ISONE',
    'start_date': '2020-02-03T21:30:00+00:00'}

    genfuelmix = {'data': {'coal_marginal': '0.0',
      'coal_mw': '22',
      'hydro_marginal': '0.0',
      'hydro_mw': '1487',
      'landfill_gas_marginal': '0.0',
      'landfill_gas_mw': '30',
      'natural_gas_marginal': '1.0',
      'natural_gas_mw': '6872',
      'nuclear_marginal': '0.0',
      'nuclear_mw': '3347',
      'other_marginal': '0.0',
      'other_mw': '3',
      'refuse_marginal': '0.0',
      'refuse_mw': '394',
      'wind_marginal': '0.0',
      'wind_mw': '166',
      'wood_marginal': '0.0',
      'wood_mw': '274'},
    'dedup_key': 'generated_fuel_mix:ISONE:2020-02-03T00:00:00+00:00',
    'event_type': 'generated_fuel_mix',
    'meta': {'calculated': 'simple',
      'inserted_at': '2020-02-03T00:04:39.570473Z',
      'raw_start_date': '2020-02-02T18:52:48-05:00',
      'scraped_at': '2020-02-03T00:04:36.093340Z',
      'source': 'singularity-scrapers'},
    'region': 'ISONE',
    'start_date': '2020-02-03T00:00:00+00:00'}

    raw_genfuelmix = {'data': {'BeginDate': '2020-02-02T19:03:13.000-05:00',
      'FuelCategory': 'Wind',
      'FuelCategoryRollup': 'Renewables',
      'GenMw': 160,
      'MarginalFlag': 'N'},
    'dedup_key': 'raw.generated_fuel_mix:ISONE:Wind:2020-02-02T19:03:13.000-05:00',
    'event_type': 'raw.generated_fuel_mix',
    'meta': {'inserted_at': '2020-02-03T00:04:44.159206Z',
      'scraped_at': '2020-02-03T00:04:35.815406Z',
      'source': 'https://webservices.iso-ne.com/api/v1.1/genfuelmix/day/{}.json'},
    'region': 'ISONE',
    'start_date': '2020-02-03T00:03:13+00:00'}


Import Export
^^^^^^^^^^^^^^

Most regions will also have information on the energy that they are exporting/importing to and from their neighboring regions.
Similar to genfuelmix, we have raw and processed events for this:

 - raw.import_export: (not all regions will have this) the raw data that was scraped from the BA's website.
 - import_export: (not all regions will have this) this data is normalized to 5 minutes and has consistent
   naming in the `data` fields
 - region_flow: (not all regions will have this) this data takes the import_export events and finds the regions
   that connect at the different "nodes" in the grid. Once the region is found, the import/export is summed for
   each region. If you request NYISO's region_flow, for example, you will see what NYISO thinks they exported and
   imported from a neighboring region, such as PJM. If you request PJM's region flow, you will see what PJM thinks
   they exported and imported from NYISO. Unfortunately, these don't always line up

Here are three example events::

    raw_import_export = {'data': {'ActualFlow': -370.829,
      'BeginDate': '2020-02-02T19:00:00.000-05:00',
      'CurrentSchedule': -335,
      'ExportLimit': 200,
      'ImportLimit': -1000,
      'Location': {'$': '.I.SALBRYNB345 1', '@LocId': '4010'},
      'Purchase': -345,
      'Sale': 10,
      'TotalExports': 2530,
      'TotalImports': -3571},
    'dedup_key': 'raw.import_export:ISONE:4010:2020-02-03T00:00:00+00:00',
    'event_type': 'raw.import_export',
    'meta': {'inserted_at': '2020-02-03T00:11:15.580468Z',
      'scraped_at': '2020-02-03T00:10:54.632925Z',
      'source': 'https://webservices.iso-ne.com/api/v1.1/fiveminuteexternalflow/day/{}.json'},
    'region': 'ISONE',
    'start_date': '2020-02-03T00:00:00+00:00'}

    import_export = {'data': {'actual_flow': -1372.922,
      'current_schedule': -1400,
      'export_limit': 1200,
      'import_limit': -1400,
      'location_id': '4012',
      'location_name': '.I.HQ_P1_P2345 5',
      'sale': 0,
      'total_exports': 2530,
      'total_imports': -3571},
    'dedup_key': 'import_export:ISONE:4012:2020-02-03T00:00:00+00:00',
    'event_type': 'import_export',
    'meta': {'calculated': 'simple',
      'inserted_at': '2020-02-03T00:11:05.452340Z',
      'raw_start_date': '2020-02-02T19:00:00-05:00',
      'scraped_at': '2020-02-03T00:10:55.331976Z',
      'source': 'singularity-scrapers'},
    'region': 'ISONE',
    'start_date': '2020-02-03T00:00:00+00:00'}

    region_flow = {'data': {'HQ': {'export': 0, 'import': 1594.922},
      'NB': {'export': 0, 'import': 313.265},
      'NYISO': {'export': 2.424, 'import': 608.039}},
    'dedup_key': 'region_flow:ISONE:2020-02-03 14:25:00+00:00',
    'event_type': 'region_flow',
    'meta': {'calculated_at': '2020-02-03T16:21:02.877985Z',
      'inserted_at': '2020-02-03T16:21:04.648359Z',
      'source': 'singularity-scrapers'},
    'region': 'ISONE',
    'start_date': '2020-02-03T14:25:00+00:00'}


Carbon Intensity
^^^^^^^^^^^^^^^^

Some of the most important data that Singularity provides is the carbon intensity data.
This data shows the different rates of carbon emissions based on energy usage and source.
The currently available fields are `generated_rate` and `marginal_rate`. Every region that has
genfuelmix events will also have carbon_intensity events. There are two different types of
carbon_intensity events that you can find.

 - carbon_intensity
 - forecast.carbon_intensity

Both have the same fields in their data, except that the forecast event also has forecast_horizon_in_minutes.
Here are two example events::

    carbon_intensity = {'data': {'generated_rate': 546.9931389673679, 'marginal_rate': 866.888301},
    'dedup_key': 'ISONE:carbon_intensity:2020-02-03T00:00:00+00:00',
    'event_type': 'carbon_intensity',
    'meta': {'inserted_at': '2020-02-03T00:04:38.515382Z',
      'marginal_source': 'ISONE:marginal_fuel_mix:2020-02-03T00:00:00+00:00',
      'raw_start_date': '2020-02-02T18:52:48-05:00',
      'source': 'generated_fuel_mix:ISONE:2020-02-03T00:00:00+00:00',
      'unit': 'lbs/MWh'},
    'region': 'ISONE',
    'start_date': '2020-02-03T00:00:00+00:00'}

    forecasted_intensity = {'data': {'forecast_horizon_in_minutes': 5,
      'generated_rate': 546.8497036624233,
      'marginal_rate': 866.888301},
    'dedup_key': 'ISONE:forecast.carbon_intensity:5I:2020-02-03T00:00:00+00:00',
    'event_type': 'forecast.carbon_intensity',
    'meta': {'forecast_horizon_in_minutes': 5,
      'inserted_at': '2020-02-03T23:56:41.655589Z',
      'marginal_source': 'forecast.marginal_fuel_mix:ISONE:5I:2020-02-02T19:00:00-05:00',
      'raw_start_date': '2020-02-02T18:55:00-05:00',
      'source': 'forecast.generated_fuel_mix:ISONE:5I:2020-02-02T19:00:00-05:00',
      'unit': 'lbs/MWh'},
    'region': 'ISONE',
    'start_date': '2020-02-03T00:00:00+00:00'}

The `meta` fields refer to the events that were used to calculate the intensity. In both, you will see
`source`, which was used to calculate the generated rate, and `marginal_source`, which was used to calculate
the marginal rate. Both of those values are a dedup_key of another event which can be used to find that event.


Plant Operation
^^^^^^^^^^^^^^^^

Singularity also offers historical information on all large energy plants in the US for the year 2019.
The event type to query is:

 - raw.plant_operation: event time put on 1 hour mark for many plants.
 - raw.plant_operation_summary: event time put on midnight UTC time of the start of the month for many plants.

Here is an example event::

    raw_plant_op = {'data': {'CO2 (tons)': 0.0,
      'FACILITY_NAME': 'Mystic',
      'GLOAD (MW)': 0.0,
      'GLOAD (MWH)': 0.0,
      'HEAT_INPUT (mmBtu)': 0.0,
      'NOX (lbs)': 0.0,
      'OP_DATE_TIME': '2019-03-23T00:00:00+00:00',
      'ORISPL_CODE': 1588,
      'SO2 (lbs)': 0.0,
      'STATE': 'MA'},
    'dedup_key': 'USA.MA:raw.plant_operation:1588:2019-03-23T00:00:00+00:00',
    'event_type': 'raw.plant_operation',
    'meta': {'inserted_at': '2020-01-31T21:29:15.073200Z',
      'source': 'https://ampd.epa.gov/ampd/'},
    'region': 'USA.MA',
    'start_date': '2019-03-23T00:00:00+00:00'}

    raw_plant_op_monthly = {'data': {'AER Fuel Type Code': 'OTH',
                'Census Region': 'NEW',
                'Combined Heat And Power Plant': 'N',
                'EIA Sector Number': '2',
                'Elec Fuel Consumption MMBtu': '0',
                'Elec_MMBtu': '.',
                'Elec_Quantity': '.',
                'Electric Fuel Consumption Quantity': '489',
                'MMBtuPer_Unit': '.',
                'NAICS Code': '22',
                'NERC Region': 'NPCC',
                'Net Generation (Megawatthours)': '-85',
                'Netgen': '.',
                'Nuclear Unit Id': '.',
                'Operator Id': '62122',
                'Operator Name': 'Minuteman Eenergy Storage, LLC',
                'Physical Unit Label': 'megawatthours',
                'Plant Id': '62644',
                'Plant Name': 'Minuteman Energy Storage',
                'Plant State': 'MA',
                'Quantity': '.',
                'Reported Fuel Type Code': 'MWH',
                'Reported Prime Mover': 'BA',
                'Reserved': '',
                'Sector Name': 'NAICS-22 Non-Cogen',
                'Tot_MMBtu': '.',
                'Total Fuel Consumption MMBtu': '0',
                'Total Fuel Consumption Quantity': '489',
                'YEAR': '2019'},
      'dedup_key': 'USA.MA:raw.plant_operation_summary:EIA923,EIA860:62644.BA,MWH:2018-12-31T19:00:00+00:00',
      'event_type': 'raw.plant_operation_summary',
      'meta': {'inserted_at': '2020-03-09T20:51:44.399465Z',
                'label descriptions': {'Elec Fuel Consumption': 'Year-To-Date',
                                      'Elec_MMBtu': 'Quantity Consumed For '
                                                    'Electricity (MMBtu)',
                                      'Elec_Quantity': 'Quantity Consumed In '
                                                        'Physical Units For Electric '
                                                        'Generation',
                                      'Electric Fuel Consumption': 'Year-To-Date',
                                      'MMBtuPer_Unit': 'Heat Content Of Fuels '
                                                        '(MMBtu Per Unit)',
                                      'Net Generation': 'Year-To-Date',
                                      'Netgen': 'Electricity Net Generation (MWh)',
                                      'Quantity': 'Total Quantity Consumed In '
                                                  'Physical Units (Consumed For '
                                                  'Electric Generation And Useful '
                                                  'Thermal Output)',
                                      'Tot_MMBtu': 'Total Fuel Consumed (MMBtu)',
                                      'Total Fuel Consumption': 'Year-To-Date'},
                'month': 'January',
                'scraped_at': '2020-03-09T20:03:49.815828Z',
                'source': 'https://www.eia.gov/electricity/data/eia923/',
                'technical notes from EIA': 'https://www.eia.gov/electricity/monthly/pdf/technotes.pdf'},
      'region': 'USA.MA',
      'start_date': '2018-12-31T19:00:00+00:00'}

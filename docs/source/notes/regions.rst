Regions
==========

Currently, a region event is scoped to a specific "region". The definition is loosely tied to
a Balancing Authority (BA), a municipal entity that controls the flow of energy in an area that could
span multiple states, or just a part of one state. The currently supported BAs are:

 - `ISONE <https://www.iso-ne.com/>`_ (New England)
 - `NYISO <https://www.nyiso.com/>`_ (New York)
 - `PJM <https://www.pjm.com/>`_ (PA, NJ, OH, VA, and some of WV, NC, KY, IN, IL, MI)
 - `IESO <http://www.ieso.ca/>`_ (Ontario)
 - `MISO <https://www.misoenergy.org/>`_ (Mid-continent stretch from TX to Manitoba)
 - `CAISO <http://www.caiso.com/Pages/default.aspx>`_ (California and some surrounding areas)
 - `SPP <https://www.spp.org/>`_ (Most of ND, SD, NE, KS, MS, OK, and some surrounding areas)
 - `BPA <https://www.bpa.gov/>`_ (Washington)

For more information on the other balancing authorities, take a look at the
`EIA's page <https://www.eia.gov/todayinenergy/detail.php?id=27152>`_ on them.

These regions will have the richest amount of events. We also have historical information
on the 2019 plant emissions for all US-based energy plants that are part of `ADMP <https://ampd.epa.gov/ampd/>`_.
The regions for those can be found as "USA.(2 letter state code)", for any state (e.g. USA.SC for all
South Carolina based plants) and `raw.plant_operation` is the event_type.

We also have similar data that reports the plant generation for most plants in the US. The
2019 `EIA 923 <https://www.eia.gov/electricity/data/eia923/>`_ data is available. The regions for the plants
are "USA.(2 letter state code)" and the data is a monthly summary recorded at the first hour of every month.
E.g. to get January's summary, request the data for Jan 1, 2019 at midnight UTC.

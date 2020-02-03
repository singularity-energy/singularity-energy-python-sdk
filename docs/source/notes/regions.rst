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

These regions will have the richest amount of events. We also have historical information
on the 2019 plant emissions for all US-based energy plants. The regions for those can be found as
"USA.(2 letter state code)", for any state (e.g. USA.SC for all South Carolina based plants) and
`raw.plant_operation` is the event_type
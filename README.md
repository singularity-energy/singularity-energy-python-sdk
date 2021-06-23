# Python Singularity Energy SDK

This package is the Python integration for real time energy data powered by [Singularity](https://www.singularity.energy)

Read the full documentation on our [readthedocs page](https://singularity-energy.readthedocs.io/en/latest/)

## Examples

Here are a couple examples you can use to get started:


```
from datetime import datetime, timedelta
from singularity import SingularityAPI, Regions, APIException


singularity = SingularityAPI('API_KEY')


end = datetime.utcnow()
start = end - timedelta(hours=4)
events, pagination = singularity.search_region_events(
  Regions.ISONE,
  'carbon_intensity',
  start.isoformat() + 'Z',
  end.isoformat() + 'Z'
)
```
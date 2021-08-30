verbose = 0
tigo_system_id     = 0
tigo_api_key       = ''
tigo_power_entity  = 0
tigo_energy_entity = 0
pvoutput_system_id = 0
pvoutput_api_key   = ''

import json
import csv
import requests
from datetime import datetime, timedelta
from pytz import timezone
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from time import sleep

# retry failed http requests up to 10 times
retries = Retry(total=10, backoff_factor=2, status_forcelist=[ 500, 502, 503, 504 ])
req = requests.Session()
req.mount('https://', HTTPAdapter(max_retries=retries))

if verbose:
    time = datetime.now(timezone('US/Eastern'))
    dt_string = time.strftime("%Y-%m-%dT%H:%M:%S")
    print( 'Now: ' + dt_string )

time = datetime.now(timezone('US/Eastern')) - timedelta(minutes=15)
dt_string = time.strftime("%Y-%m-%dT%H:%M:00")

url = "https://api2.tigoenergy.com/api/v3/data/aggregate?system_id=%d&start=%s&end=%s" % (tigo_system_id, dt_string, dt_string)

if verbose:
    print( 'Requested time: ' + dt_string )

headers = {
        'Authorization': "Bearer %s" % (tigo_api_key)
        }

# attempt to read energy values for up to 1 hour
for i in range(1,60):
    try:
        r = req.get(url, headers=headers)

        reader = csv.DictReader(r.text.split('\n'))
        for row in reader:
            power = row[str(tigo_power_entity)]
            energy = row[str(tigo_energy_entity)]
        # throw NameError if power or energy are not defined
        power
        energy
        if verbose:
            print( "Power: %s, Energy: %s" % (power, energy) )
    except (NameError, KeyError) as e:
        if verbose:
            print( err )
            print( "No value received. Retrying in 1 minute..." )
        sleep(60)
        continue
    break

#post to pvoutput.org
url = "https://pvoutput.org/service/r2/addstatus.jsp"

headers = {
        'X-Pvoutput-Apikey': pvoutput_api_key,
        'X-Pvoutput-SystemId': str(pvoutput_system_id)
        }

data = {
        'd': time.strftime("%Y%m%d"),
        't': time.strftime("%H:%M"),
        'c1': 1,
        'v1': energy,
        'v2': max(0, float(power))
        }

r = req.post(url, headers=headers, data=data)
if verbose:
    print( r.text )

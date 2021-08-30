Steps:

- Create accounts on TigoEnergy.com and PVOutput.org
- Configure the solar array on both platforms. Make sure your system layout shows the energy production and power meters you want to use.
- Set up an api key on pvoutput.org
- Create a bearer token with the Tigo Energy API:
  - curl -v -u "{username}:{password}" "https://api2.tigoenergy.com/api/v3/users/login"
- Fetch an energy update and find the value keys you need from the CSV output:
  - curl -v -H 'Authorization: Bearer <your_bearer_token>' "https://api2.tigoenergy.com/api/v3/data/aggregate?system_id=<your_systemid>&start=2021-09-01T12:15:00&end=2021-09-01T12:15:00"
- Update the values at the top of the tigo.py script

Once the tigo.py script is completing successfully, use cron to run it every 5 minutes while the array is generating. It will post data from "15 minutes ago" and will retry until it receives that data from the Tigo API (the Tigo API frequently gets behind by up to an hour)

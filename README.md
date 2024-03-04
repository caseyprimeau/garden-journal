# garden

## Currently does:
Weather & rainfall recording.

## Planned Features:
Garden Journal, Reminders. 

## Backend:

### get_rain.py 
Uses Open Weather API to collect weather conditions and rainfall amount for the prior hour for a given US postal code.

#### Setup:
  Create a postgres db & required tables.

  Configure .env in backend folder including database credentials, API key, and postal code. 

  Configure crontab to run get_rain.py hourly.

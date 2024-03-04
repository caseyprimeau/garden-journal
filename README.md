# garden

## Currently does:
Weather & rainfall Recording.

## Planned Features:
Garden Journal, Reminders. 

## Backend:

### get_rain.py 
Uses Open Weather API to collect weather conditions and rainfall amount for prior hour for a given US postal code.

#### Setup:
  Create a postgres db & required tables.
  Configure .env in backend folder including database credentials. 
  Configure crontab to run get_rain.py hourly.

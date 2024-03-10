#Get hourly rain data (in mm) from openweathermap.org

"""
To Dos:
    x-Get API_KEY from env variable
    -Get set of postal codes from db
    x-Add Database Insert
    -Add Logging
    -Set Up Notifications for Error Handling
"""
import os
import json
import requests
import pgeocode
import psycopg2
from dotenv import load_dotenv

# Load environment variables 
load_dotenv()

# Load secrets from environment variable 
API_KEY = os.getenv('OPENWEATHER_API_KEY')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_ADDRESS = os.getenv('DB_ADDRESS')
ZIP_CODE = os.getenv('ZIP_CODE')


if not API_KEY:
  raise ValueError("OpenWeather API key not set")

# Initialize Nominatim API
nomi = pgeocode.Nominatim('us')

# Lookup geo coordinates for zip code
geo = nomi.query_postal_code(ZIP_CODE)
lat = geo.latitude
lon = geo.longitude  

# Build API request  
url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"

try:
  response = requests.get(url)
  response.raise_for_status()

  # Extract rain data
  data = response.json()
  rain = data['rain']['1h']

except KeyError:
  print("Rain key not found, defaulting to 0")
  rain = 0

except Exception as e:
  print(f"Error: {e}")
  rain = None

print(data)
print("=====================================")
print("Rain:")
print(rain)


#Database Insert
try:
  connection = psycopg2.connect(user=DB_USER,
                                  password=DB_PASSWORD,
                                  host = DB_ADDRESS,
                                  port="5432",
                                  database="gdnapp")
  cursor = connection.cursor()
  cursor.execute("INSERT INTO rainfall_"+ZIP_CODE+""" (datetime, amount, weather_json) VALUES (NOW(), %s, %s) """, (rain, json.dumps(data)))
  connection.commit()
  count = cursor.rowcount
  print (count, "Record inserted successfully into rainfall_"+ZIP_CODE+" table")
except (Exception, psycopg2.Error) as error :
  print("Failed to insert record into mobile table", error)
finally:
  #closing database connection.
  if(connection):
      cursor.close()
      connection.close()
      print("Database Connection Closed")


print("Done")

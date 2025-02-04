import json
import requests
import pandas as pd
import csv

station_information = 'https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information'
station_status = 'https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_status'


response = requests.get(station_information)
if 'json' in response.headers['Content-Type']:
  json_data = response.json()  
  stations_list = json_data['data']['stations']
  print(stations_list[0])


import json
import requests
import pandas as pd
import csv

station_information = 'https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information'
station_status = 'https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_status'


def save_json_to_csv(url, outpath):
  response = requests.get(url)
  if 'json' in response.headers['Content-Type']:
    json_data = response.json()['data']['stations']
    df = pd.json_normalize(json_data)
    df.to_csv(outpath, encoding='utf_8')


def get_datasets():
  save_json_to_csv(station_information, 'datasets/station_information.csv')
  save_json_to_csv(station_status, 'datasets/station_status.csv')

if __name__ == '__main__':
  get_datasets()


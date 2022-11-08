import os
from dotenv import load_dotenv
from pprint import pprint
import json

from yelpapi import YelpAPI
import pandas as pd
import numpy as np

#import datetime
#from openpyxl import Workbook, load_workbook

load_dotenv() #look in the ".env" file for env vars


YELP_API_KEY = os.getenv("YELP_API_KEY")

with YelpAPI(YELP_API_KEY, timeout_s = 3.0) as yelp_api:
    data = yelp_api.search_query(term='ice cream', location='austin, tx', limit=2)
    #data_dict = json.load(data)

df = pd.DataFrame(data["businesses"])
pprint(df.columns)


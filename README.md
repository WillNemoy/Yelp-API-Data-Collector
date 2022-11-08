# Yelp-API-Data-Collector
With the inputs of a business type and location, return data on 100 nearby businesses in an Excel workbook.


## Setup

Create and activate a virtual environment:

```sh
conda create -n yahooAPI-env python=3.8

conda activate yahooAPI-env
```

Install package dependencies:

```sh
pip install -r requirements.txt
```

## Configuration


[Obtain an API Key](https://www.alphavantage.co/support/#api-key) from AlphaVantage.

Then create a local ".env" file and provide the key like this:

```sh
# this is the ".env" file...

ALPHAVANTAGE_API_KEY="_________"
```



## Usage

Run an example script:

```sh
python -m app.my_script
```

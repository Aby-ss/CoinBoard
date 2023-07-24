import requests

from rich import print, box
from rich.panel import Panel
from rich.traceback import install
install(show_locals=True)


def get_daily_stock_data(api_key, symbol):
    base_url = 'https://www.alphavantage.co/query'
    function = 'TIME_SERIES_DAILY'
    output_size = 'compact'

    params = {
        'function': function,
        'symbol': symbol,
        'outputsize': output_size,
        'apikey': api_key
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if 'Error Message' in data:
            print(f"Error: {data['Error Message']}")
        else:
            time_series = data['Time Series (Daily)']
            for date, values in time_series.items():
                print(f"Date: {date}, Open: {values['1. open']}, High: {values['2. high']}, Low: {values['3. low']}, Close: {values['4. close']}, Volume: {values['5. volume']}")
                
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        
if __name__ == "__main__":
    api_key = "78H5RH2BRNG4G5Z6"
    stock_symbol = "AAPL"  # Replace with the desired stock symbol (e.g., "AAPL" for Apple Inc.)

    get_daily_stock_data(api_key, stock_symbol)

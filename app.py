import requests
import asciichartpy

from rich import print, box
from rich.panel import Panel
from rich.traceback import install
install(show_locals=True)


def get_daily_stock_data(symbol):
    base_url = 'https://www.alphavantage.co/query'
    function = 'TIME_SERIES_DAILY'
    output_size = 'compact'

    params = {
        'function': function,
        'symbol': symbol,
        'outputsize': output_size,
        'apikey': "78H5RH2BRNG4G5Z6"
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if 'Error Message' in data:
            print(f"Error: {data['Error Message']}")
        else:
            time_series = data['Time Series (Daily)']
            dates = []
            close_prices = []

            for date, values in time_series.items():
                dates.append(date)
                close_prices.append(float(values['4. close']))

            # Create and display ASCII chart
            chart = asciichartpy.plot(close_prices, {"height": 20, "format": "{:8.2f}"})
            print(Panel(chart, title=f"Monthly Close Prices for {symbol}", border_style="bold white", box=box.SQUARE))
                
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        

stock_symbol = "AAPL"  # Replace with the desired stock symbol (e.g., "AAPL" for Apple Inc.)
get_daily_stock_data(stock_symbol)
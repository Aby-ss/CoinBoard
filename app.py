import re
import requests
import asciichartpy

from rich import print, box
from rich.panel import Panel
from rich.layout import Layout
from rich.traceback import install
install(show_locals=True)

from textual.app import App, ComposeResult
from textual.containers import HorizontalScroll, VerticalScroll
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Placeholder, Static
from textual.widgets import Header, Footer

class Header(Placeholder):
    DEFAULT_CSS = """
    Header {
        height: 3;
        dock: top;
    }
    """
    
class Footer(Placeholder):
    DEFAULT_CSS = """
    Footer {
        height: 3;
        dock: bottom;
    }
    """


class CoinBoard(App):
    CSS_PATH = "layout.css"

    def compose(self) -> ComposeResult:
        
        
        base_url = 'https://www.alphavantage.co/query'
        function = 'TIME_SERIES_DAILY'
        output_size = 'compact'

        chart_params = {
            'function': function,
            'symbol': "AAPL",
            'outputsize': output_size,
            'apikey': "78H5RH2BRNG4G5Z6"
        }

        
        response = requests.get(base_url, params=chart_params)
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
            chart = asciichartpy.plot(close_prices, {"width": 5, "height": 10, "format": "{:8.2f}"})
            # print(Panel(chart, title=f"Monthly Close Prices for {symbol}", border_style="bold white", box=box.SQUARE))
            
        company_overview_params = {
        'function': "OVERVIEW",
        'symbol': "AAPL",
        'apikey': "78H5RH2BRNG4G5Z6"
    }
            
        response = requests.get(base_url, params=company_overview_params)
        data = response.json()

        if 'Error Message' in data:
            print(f"Error: {data['Error Message']}")
        else:
            overview_text = ""
            for key, value in data.items():
                overview_text += f"{key}: {value}\n"

            # Extract important variables
            description = re.search(r"Description: (.+)", overview_text).group(1)
            sector = re.search(r"Sector: (.+)", overview_text).group(1)
            industry = re.search(r"Industry: (.+)", overview_text).group(1)
            name = re.search(r"Name: (.+)", overview_text).group(1)
            exchange = re.search(r"Exchange: (.+)", overview_text).group(1)
            currency = re.search(r"Currency: (.+)", overview_text).group(1)
            address = re.search(r"Address: (.+)", overview_text).group(1)
            asset_type = re.search(r"AssetType: (.+)", overview_text).group(1)
            
            company_overview = f"{name}\n{description}\n\nIndustry: {industry}\nSection: {sector}\nAddress: {address}\ncurrency: {currency}"
            

            
        chart_text = f"{chart}"
        company_overview_text = f"{company_overview}"
        
        yield Header("CoinBoard", classes="Header",)
        yield Footer("Empowering Investments, Simplifying Decisions!")
        yield Horizontal(
            Vertical(
                Static(f"{chart_text}"),
                Static("More Information"),
                classes="column",
            ),
            Vertical(
                Static(f"{company_overview_text}"),
                classes="column",
            ),
        )
    
        def on_mount(self) -> None:
            self.Header.styles.background = "#9932CC"


def get_company_overview(api_key, symbol):
    base_url = 'https://www.alphavantage.co/query'
    function = 'OVERVIEW'

    params = {
        'function': function,
        'symbol': symbol,
        'apikey': api_key
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if 'Error Message' in data:
            print(f"Error: {data['Error Message']}")
        else:
            overview_text = ""
            for key, value in data.items():
                overview_text += f"{key}: {value}\n"
            
            return overview_text
                
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


    
if __name__ == "__main__":
    app = CoinBoard()
    app.run()
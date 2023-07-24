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


class Taskwise(App):
    CSS_PATH = "layout.css"

    def compose(self) -> ComposeResult:
        
        
        base_url = 'https://www.alphavantage.co/query'
        function = 'TIME_SERIES_DAILY'
        output_size = 'compact'

        params = {
            'function': function,
            'symbol': "AAPL",
            'outputsize': output_size,
            'apikey': "78H5RH2BRNG4G5Z6"
        }

        
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
            # print(Panel(chart, title=f"Monthly Close Prices for {symbol}", border_style="bold white", box=box.SQUARE))

            
        column_text = f"{chart}"
        
        yield Header("CoinBoard", classes="Header",)
        yield Footer("Empowering Investments, Simplifying Decisions!")
        yield Horizontal(
            Vertical(
                Static(f"{column_text}"),
                Static(f"{column_text}"),
                classes="column",
            ),
            Vertical(
                Static(f"{column_text}"),
                classes="column",
            ),
        )
    
        def on_mount(self) -> None:
            self.Header.styles.background = "#9932CC"





    
if __name__ == "__main__":
    app = Taskwise()
    app.run()
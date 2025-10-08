from pathlib import Path
from sys import exit, stderr

import requests
from bs4 import BeautifulSoup


def get_lowest_price():
    """Fetch the lowest price from the maizetix website."""
    try:
        response = requests.get("https://www.maizetix.com/games/168", timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        header = soup.find("div", class_="info-stats-header", string="Lowest Price")
        if header:
            price_div = header.find_next_sibling("div", class_="info-stats-number")
            if price_div:
                return float(price_div.get_text().strip("$"))

        return None

    except Exception as e:
        print(f"Error: {e}", stderr)
        return None


if __name__ == "__main__":
    price_file = Path.home() / "Scratch" / "Maize-Tix-Bot" / "price.txt"
    latest_price = float(price_file.read_text().strip())

    if (price := get_lowest_price()) is not None and price != latest_price:
        print(price)
        price_file.write_text(str(price))
        exit(0)
    exit(1)

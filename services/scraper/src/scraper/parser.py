from bs4 import BeautifulSoup

def parse_listing(html):
    soup = BeautifulSoup(html, "html.parser")
    # Placeholder: adapt selectors to target site
    events = []
    for item in soup.select(".event"):
        band = item.select_one(".band").get_text(strip=True) if item.select_one(".band") else None
        date = item.select_one(".date").get_text(strip=True) if item.select_one(".date") else None
        events.append({"band": band, "date": date})
    return events

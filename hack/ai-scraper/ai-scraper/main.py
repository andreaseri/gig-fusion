from fastapi import FastAPI
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
import os, json, re, time
from datetime import datetime
from urllib.parse import urljoin

# Load .env file automatically
load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def scrape_with_playwright(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_load_state("networkidle")
        page.screenshot(path="debug.png", full_page=True)
        html = page.content()
        browser.close()
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(html)
        return html

def extract_next_page(soup: BeautifulSoup, base_url: str) -> str:
    """Try to find a 'next page' link."""
    next_link = soup.find('a', string=re.compile("Weiter|Next|›|→", re.IGNORECASE))
    if next_link and next_link.get("href"):
        href = next_link["href"]
        if href.startswith("http"):
            return href
        else:
            return urljoin(base_url, href)
    return ""

def extract_events_from_html(html: str, url: str, fixed_location: str = None) -> dict:
    """Call GPT to extract structured event JSON."""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    trimmed_text = text[:20000].strip()  # Fit within token limit

    with open("debug.txt", "w", encoding="utf-8") as f:
            f.write(trimmed_text)

    return {"events": [], "next": ""}

    print(f"Scraped {len(trimmed_text)} characters from {url}")

    # Ask GPT to extract events in a strict JSON format
    prompt = f"""
Extract all event listings from the following website text.
Each event should be represented in this JSON format:

{{
  "events": [
    {{
      "origin": "raw text line or summary that contains all event data",
      "date": "YYYY-MM-DDTHH:MM:SS",
      "band": ["Band Name 1", "Band Name 2"],
      "location": "",
      "price_eur": 0,
      "status_kind": "",
      "new_location": "",
      "status_raw": "",
      "section": "",
      "members": [],
      "genres": []
    }}
  ],
  "next": "URL to the next page if pagination exists, otherwise empty string"
}}

Rules:
- Always output valid JSON.
- `band` must be a list of strings. Try to split with separators like (,/) multiple bands if mentioned.
- `price_eur` must be a float if possible (no currency symbols).
- Use ISO date format.
{ f"""- `location` and `section` is always "{fixed_location}", unless explicitly stated otherwise.""" if fixed_location else """- `location` and `section` can be any venue or section mentioned near in the text.""" }
- `status_kind` can be "ausverkauft", "abgesagt", "verlegt", or default "verfügbar".
- If something is missing, use an empty string.
- Only include events that are live music concerts or gigs. 
- Exclude any listings that are not musical performances (e.g., theater, comedy, sports, exhibitions, parties, karaoke or festivals without specific performing bands).
- Detect if any pagination link or "next page" is mentioned in the text.
- If there is no further page or pagination link available (i.e., this is the last page), set the value of "next" to an empty string "".


Website content:
{text}
"""
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": "You are a precise event information extractor. Always output strict JSON conforming to the requested schema."},
                {"role": "user", "content": prompt}
            ]
        )

        result = completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return {"events": [], "next": ""}

    # Try to parse JSON (handle potential code blocks)
    try:
        result_clean = re.sub(r"^```json|```$", "", result).strip()
        parsed = json.loads(result_clean)
    except Exception:
        parsed = {"events": [], "next": ""}

    # Attempt pagination link detection
    next_page = extract_next_page(soup, url)
    if next_page and not parsed.get("next"):
        parsed["next"] = next_page

    return parsed

@app.post("/extract-events")
def extract_events(url: str, location: str = None):
    max_pages: int = 15
    all_events = []
    current_url = url

    for i in range(max_pages):
        print(f"Scraping page {i+1}: {current_url}")
        html = scrape_with_playwright(current_url)
        parsed = extract_events_from_html(html, current_url, fixed_location=location)
        all_events.extend(parsed.get("events", []))
        next_url = parsed.get("next", "").strip()
        if not next_url:
            print("No more pages detected — stopping.")
            break
        current_url = next_url
        time.sleep(2)  # be polite to the server

    # Save to timestamped JSON file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"concert_events_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_events, f, ensure_ascii=False, indent=2)

    return {"events_scraped": len(all_events), "file": filename}
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
from pathlib import Path
import json


def fetch_operator_html(username: str) -> str:
    url = f"https://r6.tracker.network/r6siege/profile/ubi/{username}/operators"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()

        print(f"[Scraper] Loading {url}")

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
        except PlaywrightTimeoutError:
            print(f"[Scraper] Timeout for {username}, using partial content...")

        page.wait_for_timeout(3000)
        html = page.content()
        browser.close()

    return html


def parse_operator_stats(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    table = soup.select_one("div.operators-table table")

    if not table:
        return {}

    headers = [th.get_text(strip=True) for th in table.select("thead th")]
    operators = {}

    for row in table.select("tbody tr"):
        cells = row.find_all("td")
        op_name = cells[0].get_text(strip=True)
        stats = {header: cell.get_text(strip=True) for header, cell in zip(headers[1:], cells[1:])}
        operators[op_name] = stats

    return operators


def save_player_data(username: str, html: str, data: dict):
    Path(f"{username}_operators_page.html").write_text(html, encoding="utf-8")

    with open(f"{username}_operators.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[Scraper] Saved {username} scraped files.")


def scrape_user(username: str) -> dict:
    html = fetch_operator_html(username)
    data = parse_operator_stats(html)
    save_player_data(username, html, data)
    return data

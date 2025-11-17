import os
from Scraper import scrape_user
from Analyzer import analyze
from pathlib import Path


OUTPUT_FILE = "enemy_analysis.txt"


def cleanup():
    removed = []
    for f in os.listdir("."):
        if f.endswith("_operators.json") or f.endswith("_operators_page.html"):
            os.remove(f)
            removed.append(f)
    return removed


if __name__ == "__main__":
    raw = input("Enter up to 5 usernames (comma or space separated): ").strip()

    usernames = list(dict.fromkeys(raw.replace(",", " ").split()))[:5]  # unique + max 5

    print(f"\n[Main] Processing: {', '.join(usernames)}\n")

    all_stats = {}

    for user in usernames:
        print(f"[Main] Scraping {user}...")
        all_stats[user] = scrape_user(user)

    print("\n[Main] Sending data to GPT-5.1...\n")
    result = analyze(all_stats)

    Path(OUTPUT_FILE).write_text(result, encoding="utf-8")
    print(f"📄 Saved tactical report to: {OUTPUT_FILE}")

    print("\n🧹 Cleaning temporary files...")
    removed = cleanup()
    for f in removed:
        print(f"  - Deleted {f}")

    print("\nDone.")

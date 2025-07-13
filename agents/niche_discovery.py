import requests
import json
import time
import os
from urllib.parse import quote
from pathlib import Path

# Define your seed topic
SEED_TOPIC = "best indoor plants"

# Create output path
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "data" / "keywords"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_google_suggestions(query, max_results=20):
    url = f"http://suggestqueries.google.com/complete/search?client=firefox&q={quote(query)}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    suggestions = json.loads(response.text)[1][:max_results]
    return suggestions


def filter_keywords(keywords):
    filtered = []
    for kw in keywords:
        if any(x in kw for x in ["best", "how to", "top", "guide", "review", "vs"]):
            filtered.append({
                "keyword": kw,
                "search_intent": categorize_intent(kw),
                "source": "google_suggest"
            })
    return filtered


def categorize_intent(keyword):
    if "how to" in keyword:
        return "how-to"
    elif "vs" in keyword or "compare" in keyword:
        return "comparison"
    elif "best" in keyword or "top" in keyword:
        return "buyer intent"
    else:
        return "informational"


def main():
    keywords = get_google_suggestions(SEED_TOPIC)
    print(f"🔍 Found {len(keywords)} suggestions")

    filtered_keywords = filter_keywords(keywords)
    print(f"✅ Filtered to {len(filtered_keywords)} high-value keywords")

    file_path = OUTPUT_DIR / f"{SEED_TOPIC.replace(' ', '_')}_keywords.json"
    with open(file_path, "w") as f:
        json.dump(filtered_keywords, f, indent=4)

    print(f"💾 Saved keywords to: {file_path.resolve()}")


if __name__ == "__main__":
    main()

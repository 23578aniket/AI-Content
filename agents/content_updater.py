import json
import os
from pathlib import Path
from slugify import slugify
import openai
from dotenv import load_dotenv

# Load OpenAI API Key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Config
ARTICLES_DIR = Path("data/articles/")
GSC_DATA_FILE = Path("data/logs/search_console_data.json")
MIN_CLICKS = 2
MIN_CTR = 0.01  # 1%

def load_gsc_data():
    with open(GSC_DATA_FILE, 'r') as f:
        return json.load(f)

def get_slug_from_url(url):
    return Path(url).stem.lower().replace("-", "_")

def needs_update(row):
    return row.get("clicks", 0) < MIN_CLICKS or row.get("ctr", 0.0) < MIN_CTR

def refresh_article(content, keyword):
    prompt = f"""
    Improve this blog article on: "{keyword}".
    - Expand it with new data, examples, or trends from 2024.
    - Add new H2 and H3 sections if needed.
    - Make it more engaging, with better SEO structure.
    - Keep original tone, and use markdown formatting.

    Article:
    {content}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def main():
    rows = load_gsc_data()

    for row in rows:
        query = row['keys'][0]
        url = row['keys'][1]
        slug = get_slug_from_url(url)
        md_path = ARTICLES_DIR / f"{slug}.md"

        if not md_path.exists():
            print(f"❌ Missing file for slug: {slug}")
            continue

        if not needs_update(row):
            print(f"✅ Performing OK: {slug}")
            continue

        print(f"♻️ Refreshing: {slug} ({query})")

        with open(md_path, 'r', encoding='utf-8') as f:
            old_content = f.read()

        new_content = refresh_article(old_content, query)

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"✅ Updated: {slug}")

if __name__ == "__main__":
    main()

import openai
import json
from pathlib import Path
from slugify import slugify
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Paths
KEYWORDS_FILE = Path("data/keywords/best_indoor_plants_keywords.json")
ARTICLES_DIR = Path("data/articles/")
ARTICLES_DIR.mkdir(parents=True, exist_ok=True)

def generate_blog_post(keyword: str) -> str:
    prompt = f"""
    Write a detailed, SEO-optimized blog article on: "{keyword}"

    - Use markdown formatting (## for headings, * for bullets).
    - Start with an attention-grabbing intro.
    - Use multiple H2 sections and H3 subpoints.
    - Include relevant facts, comparisons, and examples.
    - End with a FAQ or a summary + call-to-action.
    - Use a professional yet friendly tone.

    Keep it at least 1200 words.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response['choices'][0]['message']['content']

def main():
    with open(KEYWORDS_FILE, "r") as f:
        keywords = json.load(f)

    for item in keywords:
        keyword = item['keyword']
        slug = slugify(keyword)
        filename = ARTICLES_DIR / f"{slug}.md"

        if filename.exists():
            print(f"⏩ Skipping existing article: {slug}")
            continue

        print(f"✍️ Generating article for: {keyword}")
        article = generate_blog_post(keyword)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(article)

        print(f"✅ Saved: {filename.name}")

if __name__ == "__main__":
    main()

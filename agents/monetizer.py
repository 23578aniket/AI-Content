import re
from pathlib import Path
import json
from slugify import slugify

# Settings
ARTICLES_DIR = Path("data/articles/")
AFFILIATE_MAP = {
    "indoor plant": "https://amzn.to/xyz123",
    "grow light": "https://amzn.to/grow123",
    "planter": "https://amzn.to/pot123"
}
AD_PLACEHOLDER = "\n\n<!--adsense-->\n\n"

def inject_affiliate_links(content, keyword_map):
    for keyword, link in keyword_map.items():
        pattern = re.compile(rf"\b({re.escape(keyword)})\b", flags=re.IGNORECASE)
        content = pattern.sub(rf"[\1]({link})", content, count=1)
    return content

def insert_cta(content):
    cta = "\n👉 **Check our recommended gear on [Amazon](https://amzn.to/xyz123)**\n"
    return content + cta

def insert_ads(content):
    paragraphs = content.split('\n\n')
    if len(paragraphs) > 4:
        paragraphs.insert(2, AD_PLACEHOLDER)
        paragraphs.insert(len(paragraphs) // 2, AD_PLACEHOLDER)
    return '\n\n'.join(paragraphs)

def monetize_article(article_path):
    with open(article_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = inject_affiliate_links(content, AFFILIATE_MAP)
    content = insert_cta(content)
    content = insert_ads(content)

    with open(article_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"💸 Monetized: {article_path.name}")

def main():
    for article_file in ARTICLES_DIR.glob("*.md"):
        monetize_article(article_file)

if __name__ == "__main__":
    main()

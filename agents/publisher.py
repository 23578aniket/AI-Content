import requests
import os
from pathlib import Path
from slugify import slugify
from dotenv import load_dotenv
from base64 import b64encode

# Load credentials
load_dotenv()
WP_URL = os.getenv("WORDPRESS_URL") + "/wp-json/wp/v2"
WP_USER = os.getenv("WORDPRESS_USER")
WP_PASS = os.getenv("WORDPRESS_APP_PASSWORD")

# Auth
auth = (WP_USER, WP_PASS)

# Paths
ARTICLES_DIR = Path("data/articles/")
IMAGES_DIR = Path("data/images/")

def upload_media(image_path):
    headers = {
        'Content-Disposition': f'attachment; filename={image_path.name}',
        'Content-Type': 'image/png'
    }
    with open(image_path, 'rb') as img:
        response = requests.post(f"{WP_URL}/media", headers=headers, auth=auth, data=img)
    if response.status_code == 201:
        return response.json()['id']
    else:
        print("⚠️ Media upload failed:", response.text)
        return None

def publish_post(title, content, image_path=None):
    featured_image_id = upload_media(image_path) if image_path and image_path.exists() else None

    post_data = {
        "title": title,
        "slug": slugify(title),
        "content": content,
        "status": "publish",
    }

    if featured_image_id:
        post_data["featured_media"] = featured_image_id

    response = requests.post(f"{WP_URL}/posts", auth=auth, json=post_data)

    if response.status_code == 201:
        print(f"✅ Published: {title}")
    else:
        print(f"❌ Failed: {title} — {response.text}")

def main():
    for md_file in ARTICLES_DIR.glob("*.md"):
        title = md_file.stem.replace("_", " ").title()
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        image_file = IMAGES_DIR / f"{md_file.stem}.png"
        publish_post(title, content, image_file)

if __name__ == "__main__":
    main()

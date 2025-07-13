from openai import OpenAI
import json
import os
import requests
from pathlib import Path
from slugify import slugify
from dotenv import load_dotenv

# Load environment variables from .env file (e.g., OPENAI_API_KEY=your_key_here)
load_dotenv()

# Initialize the OpenAI client.
# It will automatically look for OPENAI_API_KEY in your environment variables.
# If you prefer to explicitly pass it, replace os.getenv("OPENAI_API_KEY")
# with your actual API key string: client = OpenAI(api_key="YOUR_ACTUAL_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define paths for keywords file and images directory
KEYWORDS_FILE = Path("data/keywords/best_indoor_plants_keywords.json")
IMAGES_DIR = Path("data/images/")

# Ensure the images directory exists
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

def generate_image(prompt: str, filename: str):
    """
    Generates an image using OpenAI's DALL-E API and saves it to a file.

    Args:
        prompt (str): The text prompt for image generation.
        filename (str): The base filename (without extension) for the saved image.
    """
    try:
        # Call the OpenAI image generation API
        # Using dall-e-3 for higher quality, and standard size/quality
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1, # Number of images to generate (dall-e-3 only supports 1)
            size="1024x1024", # Recommended size for dall-e-3
            quality="standard", # Can be "standard" or "hd"
            response_format="url", # Request the image as a URL
        )

        # Access the image URL correctly from the response object
        # response.data is a list of Image objects, each with a 'url' attribute
        image_url = response.data[0].url

        # Download the image content from the URL
        image_data = requests.get(image_url).content
        image_path = IMAGES_DIR / f"{filename}.png"

        # Save the image data to a PNG file
        with open(image_path, "wb") as f:
            f.write(image_data)

        print(f"🖼️ Saved image: {image_path.name}")
        return image_path # Return the path to the saved image

    except Exception as e:
        # Catch and print any errors during generation or saving
        # This will now print the full error object for better debugging
        print(f"❌ Error generating or saving image for '{filename}': {e}")
        # If it's an OpenAI API error, try to print more details
        if hasattr(e, 'response') and hasattr(e.response, 'json'):
            try:
                error_details = e.response.json()
                print(f"   OpenAI API Error Details: {json.dumps(error_details, indent=2)}")
            except Exception as json_e:
                print(f"   Could not parse error details as JSON: {json_e}")
        return None

def main():
    """
    Main function to load keywords, check for existing images,
    and generate new images as needed.
    """
    # Check if the keywords file exists
    if not KEYWORDS_FILE.exists():
        print(f"Error: Keywords file not found at {KEYWORDS_FILE}")
        print("Please ensure 'data/keywords/best_indoor_plants_keywords.json' exists.")
        return

    try:
        # Load keywords from the JSON file
        with open(KEYWORDS_FILE, "r") as f:
            keywords = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not parse JSON from {KEYWORDS_FILE}. Check file format.")
        return
    except Exception as e:
        print(f"Error reading keywords file: {e}")
        return

    # Iterate through each keyword item
    for item in keywords:
        # Ensure the 'keyword' key exists in the current item
        if 'keyword' not in item:
            print(f"Skipping item due to missing 'keyword' key: {item}")
            continue

        keyword = item['keyword']
        slug = slugify(keyword) # Create a URL-friendly slug from the keyword
        image_path = IMAGES_DIR / f"{slug}.png"

        # Check if an image for this keyword already exists
        if image_path.exists():
            print(f"⏩ Skipping existing image: {slug}")
            continue

        # --- START OF PROMPT REFINEMENT FOR CONTENT POLICY ---
        # The 'image_generation_user_error' with null message often indicates
        # content policy violation. Let's try to make prompts more generic
        # by removing potentially sensitive or problematic phrases.
        cleaned_keyword = keyword.replace("as per vastu", "").replace("for health", "").replace("for oxygen", "").strip()

        # If the cleaned keyword becomes empty or too generic after stripping,
        # fallback to a very general term to ensure a valid prompt.
        if not cleaned_keyword or "indoor plants" in cleaned_keyword.lower():
            # This check ensures we don't end up with just "indoor plants" if the original
            # keyword was already "best indoor plants" or similar.
            # A more sophisticated solution might involve a mapping or more complex parsing.
            if "indoor plants" not in cleaned_keyword.lower():
                 cleaned_keyword = "indoor plants"
            else:
                 # If it already contains "indoor plants", just use the cleaned version
                 pass


        # Construct the refined prompt for image generation
        # Focusing on a direct visual description to avoid policy triggers.
        prompt = f"A high-quality photo-realistic image of '{cleaned_keyword}'."
        # --- END OF PROMPT REFINEMENT ---

        print(f"🎨 Generating image for: {keyword} (Prompt: '{prompt}')") # Added prompt to output
        # Generate and save the image
        generate_image(prompt, slug)

if __name__ == "__main__":
    main()

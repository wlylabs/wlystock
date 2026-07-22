import json
import os
import requests
from huggingface_hub import InferenceClient
from huggingface_hub.errors import HfHubHTTPError
from config import HF_TOKEN, OUTPUT_DIR

client = InferenceClient(provider="auto", api_key=HF_TOKEN)

POLLINATIONS_URL = "https://image.pollinations.ai/prompt/{prompt}"

def load_topics(path="../prompts/topics.json"):
    with open(path, "r") as f:
        return json.load(f)

def generate_with_huggingface(prompt: str):
    return client.text_to_image(
        prompt,
        model="black-forest-labs/FLUX.1-schnell"
    )

def generate_with_pollinations(prompt: str, width=1024, height=1024):
    url = POLLINATIONS_URL.format(prompt=requests.utils.quote(prompt))
    params = {"width": width, "height": height, "nologo": "true"}
    response = requests.get(url, params=params, timeout=120)
    response.raise_for_status()

    from io import BytesIO
    from PIL import Image
    return Image.open(BytesIO(response.content))

def generate_image(prompt: str):
    try:
        print("Trying Hugging Face...")
        return generate_with_huggingface(prompt)
    except HfHubHTTPError as e:
        print(f"Hugging Face failed ({e}), falling back to Pollinations...")
        return generate_with_pollinations(prompt)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    topics = load_topics()

    for item in topics:
        print(f"Generating: {item['id']}")
        try:
            image = generate_image(item["prompt"])
            raw_path = os.path.join(OUTPUT_DIR, f"{item['id']}_raw.png")
            image.save(raw_path)
            print(f"Saved: {raw_path}")
        except Exception as e:
            print(f"Skipped {item['id']} due to error: {e}")
            continue

if __name__ == "__main__":
    main()
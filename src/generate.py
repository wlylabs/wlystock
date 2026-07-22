import json
import os
import random
import requests
from huggingface_hub import InferenceClient
from huggingface_hub.errors import HfHubHTTPError
from config import HF_TOKEN, OUTPUT_DIR, VARIANTS_PER_TOPIC

client = InferenceClient(provider="auto", api_key=HF_TOKEN)

POLLINATIONS_URL = "https://image.pollinations.ai/prompt/{prompt}"

STYLE_MODIFIERS = [
    "soft morning light",
    "golden hour lighting",
    "bright natural daylight",
    "dramatic side lighting",
    "warm ambient tones",
    "cool blue tones",
    "shot from a slightly elevated angle",
    "shot at eye level",
    "close-up detail shot",
    "wide angle composition",
    "shallow depth of field, blurred background",
    "sharp focus, high detail",
]

QUALITY_SUFFIX = "high resolution, professional stock photography, realistic, sharp focus, well composed"

def load_topics(path="../prompts/topics.json"):
    with open(path, "r") as f:
        return json.load(f)

def build_varied_prompt(base_prompt: str) -> str:
    modifier = random.choice(STYLE_MODIFIERS)
    return f"{base_prompt}, {modifier}, {QUALITY_SUFFIX}"

def generate_with_huggingface(prompt: str):
    return client.text_to_image(
        prompt,
        model="black-forest-labs/FLUX.1-schnell"
    )

def generate_with_pollinations(prompt: str, width=1024, height=1024):
    url = POLLINATIONS_URL.format(prompt=requests.utils.quote(prompt))
    params = {
        "width": width,
        "height": height,
        "nologo": "true",
        "seed": random.randint(1, 999999)
    }
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
        for variant in range(1, VARIANTS_PER_TOPIC + 1):
            varied_prompt = build_varied_prompt(item["prompt"])
            file_id = f"{item['id']}-v{variant}"
            print(f"Generating: {file_id} -> {varied_prompt}")
            try:
                image = generate_image(varied_prompt)
                raw_path = os.path.join(OUTPUT_DIR, f"{file_id}_raw.png")
                image.save(raw_path)
                print(f"Saved: {raw_path}")
            except Exception as e:
                print(f"Skipped {file_id} due to error: {e}")
                continue

if __name__ == "__main__":
    main()
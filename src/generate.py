import json
import os
import time
import requests
from config import HF_TOKEN, SD_MODEL_URL, OUTPUT_DIR

def load_topics(path="../prompts/topics.json"):
    with open(path, "r") as f:
        return json.load(f)

def generate_image(prompt: str, retries: int = 3) -> bytes:
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": prompt}

    for attempt in range(retries):
        response = requests.post(SD_MODEL_URL, headers=headers, json=payload, timeout=120)
        if response.status_code == 200:
            return response.content
        elif response.status_code == 503:
            wait = response.json().get("estimated_time", 20)
            time.sleep(wait)
        else:
            raise RuntimeError(f"Generation failed: {response.status_code} {response.text}")

    raise RuntimeError("Max retries reached for image generation")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    topics = load_topics()

    for item in topics:
        print(f"Generating: {item['id']}")
        image_bytes = generate_image(item["prompt"])
        raw_path = os.path.join(OUTPUT_DIR, f"{item['id']}_raw.png")
        with open(raw_path, "wb") as f:
            f.write(image_bytes)
        print(f"Saved: {raw_path}")

if __name__ == "__main__":
    main()
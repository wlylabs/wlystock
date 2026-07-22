import json
import os
from huggingface_hub import InferenceClient
from config import HF_TOKEN, OUTPUT_DIR

client = InferenceClient(provider="auto", api_key=HF_TOKEN)

def load_topics(path="../prompts/topics.json"):
    with open(path, "r") as f:
        return json.load(f)

def generate_image(prompt: str):
    return client.text_to_image(
        prompt,
        model="black-forest-labs/FLUX.1-schnell"
    )

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    topics = load_topics()

    for item in topics:
        print(f"Generating: {item['id']}")
        image = generate_image(item["prompt"])
        raw_path = os.path.join(OUTPUT_DIR, f"{item['id']}_raw.png")
        image.save(raw_path)
        print(f"Saved: {raw_path}")

if __name__ == "__main__":
    main()
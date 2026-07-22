import os
import time
import requests
from config import HF_TOKEN, CAPTION_MODEL_URL, OUTPUT_DIR

def get_caption(image_path: str, retries: int = 3) -> str:
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    with open(image_path, "rb") as f:
        data = f.read()

    for attempt in range(retries):
        response = requests.post(CAPTION_MODEL_URL, headers=headers, data=data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            return result[0]["generated_text"]
        elif response.status_code == 503:
            wait = response.json().get("estimated_time", 15)
            time.sleep(wait)
        else:
            raise RuntimeError(f"Captioning failed: {response.status_code} {response.text}")

    raise RuntimeError(f"Max retries reached for captioning: {image_path}")

def main():
    captions = {}
    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith("_final.jpg"):
            path = os.path.join(OUTPUT_DIR, filename)
            caption = get_caption(path)
            captions[filename] = caption
            print(f"Captioned {filename}: {caption}")
    return captions

if __name__ == "__main__":
    main()
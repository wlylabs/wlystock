import os
import base64
from huggingface_hub import InferenceClient
from config import HF_TOKEN, OUTPUT_DIR

client = InferenceClient(api_key=HF_TOKEN)

def get_caption(image_path: str) -> str:
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    b64_image = base64.b64encode(image_bytes).decode("utf-8")
    data_uri = f"data:image/jpeg;base64,{b64_image}"

    completion = client.chat.completions.create(
        model="Qwen/Qwen2.5-VL-7B-Instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image in one short sentence, suitable as a stock photo title."},
                    {"type": "image_url", "image_url": {"url": data_uri}}
                ]
            }
        ]
    )
    return completion.choices[0].message.content.strip()

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
import os
from huggingface_hub import InferenceClient
from config import HF_TOKEN, OUTPUT_DIR

client = InferenceClient(provider="hf-inference", api_key=HF_TOKEN)

def get_caption(image_path: str) -> str:
    result = client.image_to_text(
        image_path,
        model="Salesforce/blip-image-captioning-base"
    )
    return result.generated_text

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
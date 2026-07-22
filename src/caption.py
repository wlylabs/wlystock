import os
import base64
from huggingface_hub import InferenceClient
from huggingface_hub.errors import HfHubHTTPError
from config import HF_TOKEN, OUTPUT_DIR

client = InferenceClient(api_key=HF_TOKEN)

CANDIDATE_MODELS = [
    "Qwen/Qwen2.5-VL-7B-Instruct:novita",
    "meta-llama/Llama-3.2-11B-Vision-Instruct",
    "Qwen/Qwen2-VL-72B-Instruct",
    "zai-org/GLM-4.5V",
]

def get_caption(image_path: str) -> str:
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    b64_image = base64.b64encode(image_bytes).decode("utf-8")
    data_uri = f"data:image/jpeg;base64,{b64_image}"

    last_error = None
    for model_name in CANDIDATE_MODELS:
        try:
            print(f"Trying caption model: {model_name}")
            completion = client.chat.completions.create(
                model=model_name,
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
        except Exception as e:
            print(f"Model {model_name} failed: {e}")
            last_error = e
            continue

    raise RuntimeError(f"All caption models failed. Last error: {last_error}")

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
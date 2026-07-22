import json
import os
from PIL import Image
from config import OUTPUT_DIR, JPEG_QUALITY, RATIO_DIMENSIONS

def load_topics(path="../prompts/topics.json"):
    with open(path, "r") as f:
        return json.load(f)

def get_ratio_for_file(filename: str, topics: list) -> str:
    base_id = filename.split("-v")[0]
    for item in topics:
        if item["id"] == base_id:
            return item.get("ratio", "square")
    return "square"

def crop_to_ratio(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    target_ratio = target_w / target_h
    img_ratio = img.width / img.height

    if img_ratio > target_ratio:
        new_width = int(img.height * target_ratio)
        left = (img.width - new_width) // 2
        img = img.crop((left, 0, left + new_width, img.height))
    else:
        new_height = int(img.width / target_ratio)
        top = (img.height - new_height) // 2
        img = img.crop((0, top, img.width, top + new_height))

    return img.resize((target_w, target_h), Image.LANCZOS)

def process_image(raw_path: str, output_path: str, ratio_key: str):
    target_w, target_h = RATIO_DIMENSIONS.get(ratio_key, RATIO_DIMENSIONS["square"])
    with Image.open(raw_path) as img:
        img = img.convert("RGB")
        img = crop_to_ratio(img, target_w, target_h)
        img.save(output_path, "JPEG", quality=JPEG_QUALITY)

def main():
    topics = load_topics()
    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith("_raw.png"):
            raw_path = os.path.join(OUTPUT_DIR, filename)
            final_name = filename.replace("_raw.png", "_final.jpg")
            final_path = os.path.join(OUTPUT_DIR, final_name)
            ratio_key = get_ratio_for_file(filename, topics)
            process_image(raw_path, final_path, ratio_key)
            print(f"Processed: {final_path} ({ratio_key})")
            os.remove(raw_path)

if __name__ == "__main__":
    main()
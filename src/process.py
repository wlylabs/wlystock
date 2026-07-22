import os
from PIL import Image
from config import OUTPUT_DIR, MIN_RESOLUTION, JPEG_QUALITY

def process_image(raw_path: str, output_path: str):
    with Image.open(raw_path) as img:
        img = img.convert("RGB")
        if img.size[0] < MIN_RESOLUTION[0] or img.size[1] < MIN_RESOLUTION[1]:
            img = img.resize(MIN_RESOLUTION, Image.LANCZOS)
        img.save(output_path, "JPEG", quality=JPEG_QUALITY)

def main():
    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith("_raw.png"):
            raw_path = os.path.join(OUTPUT_DIR, filename)
            final_name = filename.replace("_raw.png", "_final.jpg")
            final_path = os.path.join(OUTPUT_DIR, final_name)
            process_image(raw_path, final_path)
            print(f"Processed: {final_path}")
            os.remove(raw_path)

if __name__ == "__main__":
    main()
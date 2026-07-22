import csv
import json
import os
from config import OUTPUT_DIR
from caption import get_caption

def load_topics(path="../prompts/topics.json"):
    with open(path, "r") as f:
        return json.load(f)

def find_topic(filename: str, topics: list):
    base_id = filename.split("-v")[0]
    for item in topics:
        if item["id"] == base_id:
            return item
    return None

def fallback_title(filename: str) -> str:
    return filename.replace("_final.jpg", "").replace("-", " ").replace("_", " ").title()

def fallback_keywords(item: dict) -> list:
    return [item["category"], "stock photo", "high quality"] if item else ["stock photo"]

def build_csv(csv_path):
    topics = load_topics()
    fieldnames = ["Filename", "Title", "Keywords", "Category", "Releases"]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for filename in sorted(os.listdir(OUTPUT_DIR)):
            if not filename.endswith("_final.jpg"):
                continue

            final_path = os.path.join(OUTPUT_DIR, filename)
            item = find_topic(filename, topics)
            category = item["category"] if item else "uncategorized"

            try:
                caption = get_caption(final_path)
                title = caption.strip().capitalize()
                words = [w.strip(".,").lower() for w in caption.split() if len(w) > 3]
                keywords = list(dict.fromkeys(words))
                keywords.insert(0, category)
                keywords = keywords[:20]
            except Exception as e:
                print(f"Captioning failed for {filename}, using fallback metadata: {e}")
                title = fallback_title(filename)
                keywords = fallback_keywords(item)

            writer.writerow({
                "Filename": filename,
                "Title": title,
                "Keywords": ", ".join(keywords),
                "Category": category,
                "Releases": ""
            })
            print(f"Added metadata: {filename} -> {title}")

def main():
    csv_path = os.path.join(OUTPUT_DIR, "metadata.csv")
    build_csv(csv_path)
    print(f"Metadata CSV saved: {csv_path}")

if __name__ == "__main__":
    main()
import csv
import json
import os
from config import OUTPUT_DIR
from caption import get_caption

def load_topics(path="../prompts/topics.json"):
    with open(path, "r") as f:
        return json.load(f)

def fallback_title(item: dict) -> str:
    return item["id"].replace("-", " ").replace("_", " ").title()

def fallback_keywords(item: dict) -> list:
    return [item["category"], "stock photo", "high quality"]

def build_csv(topics, csv_path):
    fieldnames = ["Filename", "Title", "Keywords", "Category", "Releases"]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for item in topics:
            filename = f"{item['id']}_final.jpg"
            final_path = os.path.join(OUTPUT_DIR, filename)

            if not os.path.exists(final_path):
                print(f"Skipped (file not found): {filename}")
                continue

            try:
                caption = get_caption(final_path)
                title = caption.strip().capitalize()
                words = [w.strip(".,").lower() for w in caption.split() if len(w) > 3]
                keywords = list(dict.fromkeys(words))
                keywords.insert(0, item["category"])
                keywords = keywords[:20]
            except Exception as e:
                print(f"Captioning failed for {filename}, using fallback metadata: {e}")
                title = fallback_title(item)
                keywords = fallback_keywords(item)

            writer.writerow({
                "Filename": filename,
                "Title": title,
                "Keywords": ", ".join(keywords),
                "Category": item["category"],
                "Releases": ""
            })
            print(f"Added metadata: {filename} -> {title}")

def main():
    topics = load_topics()
    csv_path = os.path.join(OUTPUT_DIR, "metadata.csv")
    build_csv(topics, csv_path)
    print(f"Metadata CSV saved: {csv_path}")

if __name__ == "__main__":
    main()
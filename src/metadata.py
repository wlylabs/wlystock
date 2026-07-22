import csv
import json
import os
from config import OUTPUT_DIR
from caption import get_caption

def load_topics(path="../prompts/topics.json")::
    with open(path, "r") as f:
        return json.load(f)

def build_title(caption: str) -> str:
    return caption.strip().capitalize()

def build_keywords(caption: str, category: str) -> list:
    words = [w.strip(".,").lower() for w in caption.split() if len(w) > 3]
    keywords = list(dict.fromkeys(words))  # remove duplicates, keep order
    keywords.insert(0, category)
    return keywords[:20]

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

            caption = get_caption(final_path)
            title = build_title(caption)
            keywords = build_keywords(caption, item["category"])

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
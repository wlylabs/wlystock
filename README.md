# WlyStock

An AI-powered stock image generation pipeline that automates image creation, caption generation, and metadata preparation for stock marketplaces.

Built to streamline the entire workflow—from prompt generation to export-ready metadata.

## Features

- AI-generated stock images
- Automatic image captioning
- CSV metadata generation
- Smart keyword extraction
- Category-based organization
- Fallback metadata support
- Batch processing
- Stock marketplace ready

## Workflow

```
Topics
   │
   ▼
Generate Images
   │
   ▼
Upscale / Final Images
   │
   ▼
AI Captioning
   │
   ▼
Keyword Extraction
   │
   ▼
metadata.csv
```

## Project Structure

```
wlystock/
├── caption.py
├── config.py
├── metadata.py
├── prompts/
│   └── topics.json
├── output/
│   ├── image-v1_final.jpg
│   ├── image-v2_final.jpg
│   └── metadata.csv
└── README.md
```

## Metadata Format

Each generated image includes:

| Field | Description |
|--------|-------------|
| Filename | Image filename |
| Title | AI-generated title |
| Keywords | Searchable keywords |
| Category | Image category |
| Releases | Model/property release information |

Example:

```csv
Filename,Title,Keywords,Category,Releases
forest-v1_final.jpg,"Sunlight through a green forest","nature, forest, trees, sunlight, landscape","Nature",
```

## How It Works

1. Load image topics.
2. Scan generated images.
3. Generate captions using AI.
4. Extract relevant keywords.
5. Apply category metadata.
6. Export everything into `metadata.csv`.

If caption generation fails, the pipeline automatically falls back to filename-based metadata, ensuring uninterrupted processing.

## Requirements

- Python 3.10+
- Pillow
- Your preferred AI caption model
- Additional dependencies listed in `requirements.txt`

## Installation

```bash
git clone https://github.com/wlylabs/wlystock.git
cd wlystock

pip install -r requirements.txt
```

## Usage

Generate metadata:

```bash
python metadata.py
```

Output:

```
output/
└── metadata.csv
```

## Use Cases

- Adobe Stock
- Shutterstock
- Freepik Contributor
- Dreamstime
- Depositphotos
- Other stock marketplaces

## Philosophy

WlyStock is designed to minimize repetitive manual work by automating the metadata creation process while keeping the workflow simple, fast, and scalable.

## License

MIT License
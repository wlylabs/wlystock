# wlystock

Automated AI stock photo pipeline — generates, processes, and captions royalty-free stock imagery on a schedule.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Generate Stock Images](https://github.com/wlylabs/wlystock/actions/workflows/generate.yml/badge.svg)](https://github.com/wlylabs/wlystock/actions/workflows/generate.yml)

## Overview

`wlystock` turns a curated prompt library into submission-ready stock photography without manual intervention. Each run samples a subset of topics, generates multiple visual variants per topic, normalizes them to standard stock aspect ratios, and produces a metadata CSV with AI-generated titles and keywords.

The entire pipeline runs unattended via GitHub Actions and publishes its output as a build artifact.

## Pipeline

```
prompts/topics.json
        │
        ▼
┌───────────────────┐   FLUX.1-schnell (Hugging Face)
│  1. generate.py   │   └── fallback: Pollinations
└───────────────────┘
        │  *_raw.png
        ▼
┌───────────────────┐   center-crop → resize (LANCZOS) → JPEG q95
│  2. process.py    │
└───────────────────┘
        │  *_final.jpg
        ▼
┌───────────────────┐   vision-language captioning → title + keywords
│  3. metadata.py   │
└───────────────────┘
        │
        ▼
   output/metadata.csv
```

### 1. Generation

`src/generate.py` randomly samples `TOPICS_PER_RUN` topics from the prompt library and renders `VARIANTS_PER_TOPIC` images for each. Every variant appends a randomly chosen style modifier (lighting, camera angle, depth of field) plus a shared quality suffix, so repeated runs on the same topic yield genuinely different photographs rather than near-duplicates.

Images are requested from `black-forest-labs/FLUX.1-schnell` through the Hugging Face Inference API. If that call fails, the pipeline transparently falls back to Pollinations with randomized seeds and up to three retries.

### 2. Processing

`src/process.py` reads each topic's declared `ratio` and center-crops the raw render to the matching target, then resamples with LANCZOS and encodes to JPEG at quality 95:

| Ratio       | Output resolution | Megapixels |
| ----------- | ----------------- | ---------- |
| `square`    | 2400 × 2400       | 5.8 MP     |
| `landscape` | 2560 × 1707       | 4.4 MP     |
| `portrait`  | 1707 × 2560       | 4.4 MP     |

Raw PNGs are deleted once processed, so only the final deliverables remain.

### 3. Metadata

`src/metadata.py` captions every finished image using a vision-language model, then derives a stock-style title and a keyword list (capped at 20, prefixed with the topic category). Four caption models are tried in order, so a single unavailable endpoint doesn't stall the run:

1. `Qwen/Qwen2.5-VL-7B-Instruct:novita`
2. `meta-llama/Llama-3.2-11B-Vision-Instruct`
3. `Qwen/Qwen2-VL-72B-Instruct`
4. `zai-org/GLM-4.5V`

If all four fail, the image still ships — the filename and category are used to synthesize fallback metadata.

The result is written to `output/metadata.csv` with the columns most stock agencies expect:

```csv
Filename,Title,Keywords,Category,Releases
biz-01-v1_final.jpg,A laptop and coffee cup on a wooden desk,"business, laptop, coffee, desk, wooden",business,
```

## Prompt library

`prompts/topics.json` holds 41 curated topics across 9 categories:

| Category   | Topics | Category  | Topics |
| ---------- | ------ | --------- | ------ |
| nature     | 7      | home      | 4      |
| food       | 6      | travel    | 4      |
| business   | 5      | abstract  | 3      |
| health     | 5      | education | 3      |
| technology | 4      |           |        |

Each entry declares an `id`, a `prompt`, a `category`, and a target `ratio`:

```json
{
  "id": "biz-01",
  "prompt": "flat lay of laptop keyboard closed, coffee cup, notebook and pen on wooden desk, top-down view, minimalist workspace",
  "category": "business",
  "ratio": "square"
}
```

Prompts are written to avoid identifiable faces, trademarks, and other release-requiring subjects — people appear only as silhouettes or from behind.

Adding a topic requires no code changes: append an object with a unique `id` and it enters the sampling pool on the next run.

## Getting started

### Requirements

- Python 3.11 or newer
- A [Hugging Face access token](https://huggingface.co/settings/tokens) with inference permissions

### Installation

```bash
git clone https://github.com/wlylabs/wlystock.git
cd wlystock
pip install -r requirements.txt
```

### Configuration

Set your token via environment variable or a `.env` file:

```bash
export HF_TOKEN="hf_..."
```

Without `HF_TOKEN`, image generation falls back to Pollinations and captioning falls back to filename-derived metadata.

### Running locally

The scripts resolve `prompts/topics.json` as a path relative to the working directory, so run them from `src/`:

```bash
cd src
python generate.py    # renders raw PNGs into src/output/
python process.py     # crops, resizes, and encodes to JPEG
python metadata.py    # captions images and writes metadata.csv
```

Each stage is independent and operates on whatever files the previous stage left behind — you can re-run `process.py` or `metadata.py` without regenerating images.

## Configuration reference

All tunables live in `src/config.py`:

| Setting              | Default                         | Description                             |
| -------------------- | ------------------------------- | --------------------------------------- |
| `HF_TOKEN`           | `$HF_TOKEN`                     | Hugging Face inference token            |
| `OUTPUT_DIR`         | `output`                        | Destination for images and metadata     |
| `JPEG_QUALITY`       | `95`                            | JPEG encoding quality                   |
| `VARIANTS_PER_TOPIC` | `2`                             | Images rendered per selected topic      |
| `TOPICS_PER_RUN`     | `5`                             | Topics sampled per run                  |
| `RATIO_DIMENSIONS`   | see [Processing](#2-processing) | Target resolution for each aspect ratio |

With the defaults, a single run produces up to 10 images.

## Automation

The `Generate Stock Images` workflow runs daily at **02:00 UTC** and can also be triggered manually from the Actions tab.

```yaml
on:
  workflow_dispatch:
  schedule:
    - cron: "0 2 * * *"
```

Every stage after generation uses `if: always()`, so partial failures still yield whatever images completed successfully. Results are uploaded as the artifact `stock-images-<run_number>` (JPEGs plus `metadata.csv`) with a 7-day retention window.

### Setup

Add your token as a repository secret named `HF_TOKEN` under **Settings → Secrets and variables → Actions**.

## Design notes

**Failure isolation.** No single failure aborts a run. Generation falls back across providers, captioning falls back across models and then to filename-derived metadata, and per-image exceptions are caught so one bad render never costs you the other nine.

**Variant diversity.** Style modifiers are sampled per variant rather than per topic, and Pollinations requests carry random seeds — the same prompt reliably yields distinct compositions across runs.

**Stateless output.** Generated assets are never committed. Each run is self-contained and publishes through the Actions artifact store, keeping the repository to prompts and code.

## Project structure

```
wlystock/
├── .github/workflows/
│   ├── generate.yml       # scheduled generation pipeline
│   └── main.yml           # identical pipeline definition
├── prompts/
│   └── topics.json        # curated prompt library
├── src/
│   ├── config.py          # tunables and environment configuration
│   ├── generate.py        # stage 1 — image generation
│   ├── process.py         # stage 2 — cropping, resizing, encoding
│   ├── caption.py         # vision-language captioning client
│   └── metadata.py        # stage 3 — CSV metadata assembly
├── requirements.txt
└── LICENSE
```

## Contributing

Contributions are welcome — new prompt topics, additional output ratios, and support for other generation backends are all useful directions.

1. Fork the repository and create a feature branch.
2. Keep prompts free of identifiable people, logos, and trademarked subjects.
3. Verify each pipeline stage runs cleanly from `src/` before opening a pull request.

## License

Released under the [MIT License](LICENSE). © 2026 wlylabs.

Generated images inherit the terms of their upstream model providers — review the [FLUX.1-schnell](https://huggingface.co/black-forest-labs/FLUX.1-schnell) license and [Pollinations](https://pollinations.ai) terms before commercial redistribution.

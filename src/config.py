import os

HF_TOKEN = os.environ.get("HF_TOKEN")
SD_MODEL_URL = "https://router.huggingface.co/models/black-forest-labs/FLUX.1-dev"
CAPTION_MODEL_URL = "https://router.huggingface.co/hf-inference/models/Salesforce/blip-image-captioning-base"

OUTPUT_DIR = "output"
MIN_RESOLUTION = (2400, 2400)
JPEG_QUALITY = 95
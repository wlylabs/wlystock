import os

HF_TOKEN = os.environ.get("HF_TOKEN")
SD_MODEL_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
CAPTION_MODEL_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"

OUTPUT_DIR = "output"
MIN_RESOLUTION = (2400, 2400)
JPEG_QUALITY = 95
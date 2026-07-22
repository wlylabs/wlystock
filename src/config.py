import os

HF_TOKEN = os.environ.get("HF_TOKEN")

OUTPUT_DIR = "output"
JPEG_QUALITY = 95
VARIANTS_PER_TOPIC = 2
TOPICS_PER_RUN = 5

RATIO_DIMENSIONS = {
    "square": (2400, 2400),
    "landscape": (2560, 1707),
    "portrait": (1707, 2560),
}
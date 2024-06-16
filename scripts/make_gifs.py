# extract first frame and save as {filename}-stop.gif

import os
from PIL import Image

INPUT_DIR = "static/tutorial/"
OUTPUT_DIR = "nogit/output/"

INPUT = [f for f in os.listdir(INPUT_DIR) if f.endswith(".gif")]


def extract(filename):
    output = OUTPUT_DIR + os.path.basename(filename).split(".")[0] + "-stop.gif"
    with Image.open(INPUT_DIR + filename) as img:
        img.seek(0)
        img.save(output)


for f in INPUT:
    extract(f)

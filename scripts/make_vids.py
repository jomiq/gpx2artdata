# converts gif to various video formats
# extract first frame and save as {filename}-stop.gif

import os
from PIL import Image
import moviepy.editor as mp

INPUT_DIR = "assets/make_vids/"
OUTPUT_DIR = "build/media/"
FORMATS = ["webm", "mp4", "gif"]
INPUT = [f for f in os.listdir(INPUT_DIR) if f.endswith(".gif")]
MAKE_STOP_FRAME = True


def gif_to(filename, formats=FORMATS):
    input_file = INPUT_DIR + filename
    name = os.path.basename(filename).split(".")[0]
    print(f"file: {input_file}")
    if "gif" in formats:
        formats = [v for v in formats if v != "gif"]
        output = OUTPUT_DIR + name + ".gif"
        with open(input_file, "rb") as gif_in, open(output, "wb") as gif_out:
            print(f"copy: {input_file} -> {output}")
            gif_out.write(gif_in.read())

        if MAKE_STOP_FRAME:
            output = OUTPUT_DIR + name + "-stop.gif"
            with Image.open(input_file) as img:
                img.seek(0)
                print(f"write: {output}")
                img.save(output)

    for format in formats:
        try:
            output = OUTPUT_DIR + name + f".{format}"
            with mp.VideoFileClip(input_file) as clip:
                print(f"write: {output}")
                clip.write_videofile(output)
        except Exception as e:
            print(f"{filename}: {e}")


if __name__ == "__main__":
    from joblib import Parallel, delayed  # noqa

    try:
        os.makedirs(OUTPUT_DIR)
    except Exception as e:
        print(e)

    Parallel(n_jobs=os.cpu_count())(delayed(gif_to)(f) for f in INPUT)

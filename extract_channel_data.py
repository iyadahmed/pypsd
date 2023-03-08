import os
import sys
from pathlib import Path
from traceback import print_exc

from PIL import Image

from pypsd.reader import read_psd


def main():
    if len(sys.argv) != 2:
        print("Expected arguments: file.psd")
        return

    psd_filepath = sys.argv[1]

    psd = read_psd(psd_filepath)
    if psd.layer_mask_info is None:
        print("Layer mask info is null")
        return

    extract_dirname = Path(psd_filepath).stem
    extract_dirpath = Path(__file__).parent / extract_dirname

    os.makedirs(extract_dirpath, exist_ok=True)

    image_index = 0
    for layer in psd.layer_mask_info.info.layers:
        width = layer.record.rect.width()
        height = layer.record.rect.height()
        for channel in layer.channels:
            data = channel.data

            try:
                im = Image.frombytes("L", (width, height), data)
                im.save(extract_dirpath / f"{image_index}.png")
                image_index += 1
            except Exception:
                print_exc()


if __name__ == "__main__":
    main()

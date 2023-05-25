import argparse
import ctypes
import glob
import multiprocessing
import os
import subprocess
import sys
from typing import Set, Tuple

from PIL import Image, ImageColor

stdnull = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}


def modify_image(image_path: str, rgb_value: Tuple[int]) -> None:
    # take ownership of the images
    subprocess.run(["takeown", "/F", image_path, "/A"], check=False, **stdnull)
    subprocess.run(["icacls", image_path, "/grant", "Administrators:F"], check=False, **stdnull)

    try:
        with Image.open(image_path) as original_image:
            size = original_image.size

        with Image.new("RGB", size, rgb_value) as new_image:
            new_image.save(image_path)
    except PermissionError:
        print(f"error: permission error accessing {image_path}")


def main() -> int:
    version = "0.3.4"
    images: Set[str] = set()

    print(f"win-wallpaper v{version}")
    print("GitHub - https://github.com/amitxv\n")

    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("error: administrator privileges required")
        return 1

    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=f"win-wallpaper v{version}")
    parser.add_argument(
        "--dir",
        metavar="<directory>",
        type=str,
        help="enter the directory to apply solid wallpapers to, includes offline images",
        required=True,
    )
    parser.add_argument(
        "--rgb",
        metavar="<hex code>",
        type=str,
        help="enter the desired rgb value in hex format",
        required=True,
    )
    parser.add_argument("--win7", action="store_true", help="enables Windows 7 support")
    args = parser.parse_args()

    image_paths = (
        f"{args.dir}\\ProgramData\\Microsoft\\User Account Pictures",
        f"{args.dir}\\Windows\\Web",
        f"{args.dir}\\ProgramData\\Microsoft\\Windows\\SystemData",
    )

    if not any(os.path.exists(path) for path in image_paths):
        print("error: no folders found, invalid directory")
        return 1

    try:
        rgb_value = tuple(ImageColor.getcolor(args.rgb, "RGB"))
    except ValueError:
        print("error: invalid hex code for --rgb argument")
        return 1

    for folder_path in image_paths:
        for file_type in ("jpg", "png", "bmp"):
            for image in glob.glob(f"{folder_path}/**/*.{file_type}", recursive=True):
                images.add(image)

    pool_args = [(image, rgb_value) for image in images]
    with multiprocessing.Pool() as pool:
        pool.starmap(modify_image, pool_args)

    if args.win7:
        oobe_background_path = f"{args.dir}\\Windows\\System32\\oobe\\info\\backgrounds"
        os.makedirs(oobe_background_path, exist_ok=True)
        image = f"{oobe_background_path}\\backgroundDefault.jpg"

        try:
            with Image.new("RGB", (1920, 1080), rgb_value) as new_image:
                new_image.save(image)
        except PermissionError:
            print(f"error: permission error accessing {image}")
            return 1

    print("info: done")

    return 0


if __name__ == "__main__":
    # for packed binary
    multiprocessing.freeze_support()

    sys.exit(main())

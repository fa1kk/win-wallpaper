"""win-wallpaper"""

import glob
import subprocess
import sys
import os
import argparse
import ctypes
from PIL import Image, ImageColor


def main() -> int:
    """cli entrypoint"""

    version = "0.3.3"
    subprocess_null = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
    images = []

    print(f"win-wallpaper v{version}")
    print("GitHub - https://github.com/amitxv\n")

    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("error: administrator privileges required")
        return 1

    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=f"win-wallpaper v{version}")
    parser.add_argument("--dir", metavar="<directory>", type=str, help="enter the directory to apply solid wallpapers to, includes offline images", required=True)
    parser.add_argument("--rgb", metavar="<hex code>", type=str, help="enter the desired rgb value in hex format", required=True)
    parser.add_argument("--win7", action="store_true", help="enables Windows 7 support")
    args = parser.parse_args()

    image_paths = [
        f"{args.dir}\\ProgramData\\Microsoft\\User Account Pictures",
        f"{args.dir}\\Windows\\Web",
        f"{args.dir}\\ProgramData\\Microsoft\\Windows\\SystemData"
    ]

    if not any(os.path.exists(x) for x in image_paths):
        print("error: no folders found, invalid directory")
        return 1

    try:
        rgb_value = ImageColor.getcolor(args.rgb, "RGB")
    except ValueError:
        print("error: invalid hex code for --rgb argument")
        return 1

    for folder_path in image_paths:
        for file_type in ["jpg", "png", "bmp"]:
            for i in glob.glob(f"{folder_path}/**/*.{file_type}", recursive=True):
                if i not in images:
                    images.append(i)

    for image in images:
        # take ownership of the images
        subprocess.run(["takeown", "/F", image, "/A"], check=False, **subprocess_null)
        subprocess.run(["icacls", image, "/grant", "Administrators:F"], check=False, **subprocess_null)

        try:
            original = Image.open(image)
            new = Image.new("RGB", original.size, ImageColor.getcolor(args.rgb, "RGB"))
            new.save(image)
        except PermissionError:
            print(f"error: permission error accessing {image}")

    if args.win7:
        oobe_background_path = f"{args.dir}\\Windows\\System32\\oobe\\info\\backgrounds"
        os.makedirs(oobe_background_path, exist_ok=True)
        new = Image.new("RGB", (1920, 1080), rgb_value)
        new.save(f"{oobe_background_path}\\backgroundDefault.jpg")

    print("info: done")

    return 0


if __name__ == "__main__":
    sys.exit(main())

import argparse
import ctypes
import glob
import multiprocessing
import os
import subprocess
import sys
import winreg
from collections.abc import Callable
from typing import Any

from PIL import Image, ImageColor


def add_registry_key(
    path: str,
    key_name: str,
    value: str | int,
    value_type: int,
) -> Any | None:
    with winreg.CreateKey(
        winreg.HKEY_LOCAL_MACHINE,
        path,
    ) as key:
        winreg.SetValueEx(key, key_name, 0, value_type, value)


def modify_image(image_path: str, rgb_value: tuple[int]) -> None:
    # take ownership of the images
    subprocess.run(
        ["takeown", "/F", image_path, "/A"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        ["icacls", image_path, "/grant", "Administrators:F"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        with Image.open(image_path) as original_image:
            size = original_image.size

        with Image.new("RGB", size, rgb_value) as new_image:
            new_image.save(image_path)
    except PermissionError:
        print(f"error: permission error accessing {image_path}")


def main() -> int:  # noqa: C901, PLR0912, D103
    version = "0.3.7"
    images: set[str] = set()

    print(
        f"win-wallpaper Version {version} - GPLv3\nGitHub - https://github.com/amitxv\n",
    )

    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("error: administrator privileges required")
        return 1

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        action="version",
        version=f"win-wallpaper v{version}",
    )
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
    parser.add_argument(
        "--offline",
        action="store_true",
        help="indicates that the image is mounted offline",
    )
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
        rgb_value = ImageColor.getcolor(args.rgb, "RGB")
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

    print("info: images replaced successfully")

    oem_background: Callable[[str], None] = lambda hive: add_registry_key(
        f"{hive}\\Microsoft\\Windows\\CurrentVersion\\Authentication\\LogonUI\\Background",
        "OEMBackground",
        1,
        winreg.REG_DWORD,
    )

    use_default_tile: Callable[[str], None] = lambda hive: add_registry_key(
        f"{hive}\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer",
        "UseDefaultTile",
        1,
        winreg.REG_DWORD,
    )

    if args.offline:
        subprocess.run(
            [
                "reg.exe",
                "load",
                "HKLM\\TempHive",
                f"{args.dir}\\Windows\\System32\\config\\SOFTWARE",
            ],
            check=False,
        )
        use_default_tile("TempHive")

        if args.win7:
            oem_background("TempHive")

        subprocess.run(["reg.exe", "unload", "HKLM\\TempHive"], check=False)

    else:
        use_default_tile("SOFTWARE")

        if args.win7:
            oem_background("SOFTWARE")

    print("info: done")

    return 0


if __name__ == "__main__":
    # for packed binary
    multiprocessing.freeze_support()

    sys.exit(main())

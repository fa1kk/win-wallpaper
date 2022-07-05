import glob
import subprocess
import sys
import os
from PIL import Image


def main():
    """CLI Entrypoint"""
    argc = len(sys.argv)
    argv = sys.argv

    version = "0.1.1"
    subprocess_null = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}

    if 1 <= argc <= 4:
        print("usage: win-wallpaper [root directory] [R] [G] [B] -W7\n")
        print(f"win-wallpaper v{version}\n")
        print("parameters:")
        print("    root directory    directory to apply solid wallpapers to, includes offline images")
        print("    R value           red value (0-255)")
        print("    G value           green value (0-255)")
        print("    B value           blue value (0-255)")
        print("    -w7               enable windows 7 support")
        return 1

    root_dir = argv[1]

    image_paths = [
        f"{root_dir}\\ProgramData\\Microsoft\\User Account Pictures",
        f"{root_dir}\\Windows\\Web",
        f"{root_dir}\\ProgramData\\Microsoft\\Windows\\SystemData"
    ]

    if not any([os.path.exists(x) for x in image_paths]):
        print("error: no folders found, invalid directory")
        return 1

    rgb_values = argv[2:5]
    # convert to int
    rgb_values = [int(x) for x in rgb_values]

    if not all([0 <= x <= 255 for x in rgb_values]):
        print("error: rgb values must be between 0-255")
        return 1

    rgb_r, rgb_g, rgb_b = rgb_values

    images = []

    for folder_path in image_paths:
        for file_type in ["jpg", "png", "bmp"]:
            for i in glob.glob(f"{folder_path}/**/*.{file_type}", recursive=True):
                if i not in images:
                    images.append(i)

    for image in images:
        # take ownership of the images
        subprocess.run(["takeown", "/F", image, "/A"], check=False, **subprocess_null)
        subprocess.run(["icacls", image, "/grant", "Administrators:(F)"], check=False, **subprocess_null)

        original = Image.open(image)
        new = Image.new("RGB", original.size, (rgb_r, rgb_g, rgb_b))
        new.save(image)

    if "-w7" in argv:
        oobe_background_path = f"{root_dir}\\Windows\\System32\\oobe\\info\\backgrounds"
        os.makedirs(oobe_background_path, exist_ok=True)
        new = Image.new('RGB', (1920, 1080), (rgb_r, rgb_g, rgb_b))
        new.save(f"{oobe_background_path}\\backgroundDefault.jpg")

    return 0

if __name__ == "__main__":
    main()

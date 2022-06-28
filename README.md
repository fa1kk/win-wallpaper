## win-wallpaper

CLI tool to replace the default wallpapers and user icons in Windows with a solid color.

Contact: https://twitter.com/amitxv

## Usage

```
usage: win-wallpaper <root directory> <R> <G> <B>

win-wallpaper

parameters:
    root directory    directory to apply solid wallpapers to, includes offline images
    R value           red value (0-255)
    G value           red value (0-255)
    B value           red value (0-255)
```

- Examples
    - ``win-wallpaper "C:" 0 0 0`` will replace the wallpapers on the current install with solid black images.
    - ``win-wallpaper "C:\temp" 160 30 230`` will replace the wallpapers in the mounted image ``C:\temp`` with solid purple images.

Use [this website](https://www.rapidtables.com/web/color/RGB_Color.html) to get the desired RGB values.
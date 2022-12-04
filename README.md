# win-wallpaper

Replace the default wallpapers and user icons in Windows with a customizable solid color

Contact: <https://twitter.com/amitxv>

## Usage

```txt
usage: win-wallpaper.py [-h] [--version] --dir <directory> --rgb <hex code> [--win7]

optional arguments:
  -h, --help         show this help message and exit
  --version          show program's version number and exit
  --dir <directory>  enter the directory to apply solid wallpapers to, includes offline images
  --rgb <hex code>   enter the desired rgb value in hex format
  --win7             enables Windows 7 support
```

- Examples

    - **win-wallpaper --dir "C:" --rgb #000000** will replace the wallpapers on the current install with solid black images
    - **win-wallpaper --dir "C:\temp" --rgb #A01EE6** will replace the wallpapers in the mounted image **C:\temp** with solid purple images

- Use [this website](https://www.rapidtables.com/convert/color/rgb-to-hex.html) to get the desired RGB hex code values

- This registry key may be required on Windows 7

    ```txt
    [HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI\Background]
    "OEMBackground"=dword:00000001
    ```

- This registry key may be required on Windows 7+

    ```txt
    [HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer]
    "UseDefaultTile"=dword:00000001
    ```

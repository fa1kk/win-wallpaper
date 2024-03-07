function main() {
    if (Test-Path ".\build\") {
        Remove-Item -Path ".\build\" -Recurse -Force
    }

    # entrypoint relative to .\build\pyinstaller\
    $entryPoint = "..\..\win_wallpaper\main.py"

    # pack executable
    New-Item -ItemType Directory -Path ".\build\pyinstaller\"
    Push-Location ".\build\pyinstaller\"
    pyinstaller $entryPoint --onefile --name win-wallpaper
    Pop-Location

    return 0
}

$_exitCode = main
Write-Host # new line
exit $_exitCode

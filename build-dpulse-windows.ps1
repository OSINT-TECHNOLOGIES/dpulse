$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

$pythonExe = Join-Path $repoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $pythonExe)) {
    Write-Host "Creating Python 3.11 virtual environment..."
    & py -3.11 -m venv (Join-Path $repoRoot ".venv")
}

if (-not (Test-Path $pythonExe)) {
    throw "Could not find .venv\Scripts\python.exe. Install Python 3.11 and try again."
}

Write-Host "Installing Python dependencies into the DPULSE virtual environment..."
& $pythonExe -m pip install --upgrade pip
& $pythonExe -m pip install -r (Join-Path $repoRoot "python-backend\requirements.txt")
& $pythonExe -m pip install pyinstaller pyinstaller-hooks-contrib

$pythonIdentity = (& $pythonExe -c "import sys; print(sys.executable)").Trim()
$builtwithPackagePath = (& $pythonExe -c "import builtwith, os; print(os.path.dirname(builtwith.__file__))").Trim()
$builtwithDataFile = Join-Path $builtwithPackagePath "apps.json.py"

Write-Host "Python interpreter: $pythonIdentity"
Write-Host "builtwith package:  $builtwithPackagePath"

if (-not (Test-Path $builtwithDataFile)) {
    throw "builtwith is installed, but its data file was not found: $builtwithDataFile"
}

Write-Host "Cleaning previous PyInstaller output..."
Remove-Item -Recurse -Force (Join-Path $repoRoot "python-backend\build") -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force (Join-Path $repoRoot "python-backend\dist") -ErrorAction SilentlyContinue
Remove-Item -Force (Join-Path $repoRoot "python-backend\dpulse-backend.spec") -ErrorAction SilentlyContinue

$pyinstallerArgs = @(
    "--clean",
    "--noconfirm",
    "--onefile",
    "--name", "dpulse-backend",
    "--add-data", "service;service",
    "--add-data", "datagather_modules;datagather_modules",
    "--add-data", "reporting_modules;reporting_modules",
    "--add-data", "apis;apis",
    "--add-data", "dorking;dorking",
    "--add-data", "pagesearch;pagesearch",
    "--add-data", "snapshotting;snapshotting",
    "--add-data", "$builtwithDataFile;builtwith",
    "--paths", ".",
    "--paths", "service",
    "--paths", "datagather_modules",
    "--paths", "reporting_modules",
    "--paths", "apis",
    "--paths", "dorking",
    "--paths", "pagesearch",
    "--paths", "snapshotting",
    "--hidden-import=misc",
    "--hidden-import=files_processing",
    "--hidden-import=uvicorn.logging",
    "--hidden-import=uvicorn.loops",
    "--hidden-import=uvicorn.loops.auto",
    "--hidden-import=uvicorn.protocols",
    "--hidden-import=uvicorn.protocols.http",
    "--hidden-import=uvicorn.protocols.http.auto",
    "--hidden-import=uvicorn.protocols.websockets",
    "--hidden-import=uvicorn.protocols.websockets.auto",
    "--hidden-import=uvicorn.lifespan",
    "--hidden-import=uvicorn.lifespan.on",
    "--hidden-import=selenium",
    "--hidden-import=selenium.webdriver",
    "--hidden-import=selenium.webdriver.chrome",
    "--hidden-import=selenium.webdriver.chrome.service",
    "--hidden-import=selenium.webdriver.chrome.options",
    "--hidden-import=selenium.webdriver.firefox",
    "--hidden-import=selenium.webdriver.firefox.service",
    "--hidden-import=selenium.webdriver.firefox.options",
    "--hidden-import=selenium.webdriver.edge",
    "--hidden-import=selenium.webdriver.edge.service",
    "--hidden-import=selenium.webdriver.edge.options",
    "--hidden-import=selenium.webdriver.common",
    "--hidden-import=selenium.webdriver.common.by",
    "--hidden-import=selenium.webdriver.support",
    "--hidden-import=selenium.webdriver.remote",
    "--hidden-import=selenium.webdriver.remote.webdriver",
    "--hidden-import=webdriver_manager",
    "--hidden-import=webdriver_manager.chrome",
    "--hidden-import=webdriver_manager.firefox",
    "--hidden-import=webdriver_manager.microsoft",
    "--hidden-import=webdriver_manager.core",
    "--hidden-import=webdriver_manager.core.download_manager",
    "--hidden-import=webdriver_manager.core.driver_cache",
    "--hidden-import=webdriver_manager.core.os_manager",
    "--collect-data=webdriver_manager",
    "main.py"
)

Write-Host "Building the Python backend executable..."
Push-Location (Join-Path $repoRoot "python-backend")
try {
    & $pythonExe -m PyInstaller @pyinstallerArgs
}
finally {
    Pop-Location
}

$builtBackend = Join-Path $repoRoot "python-backend\dist\dpulse-backend.exe"
if (-not (Test-Path $builtBackend)) {
    throw "PyInstaller completed without creating $builtBackend"
}

$binariesDirectory = Join-Path $repoRoot "src-tauri\binaries"
$sidecarPath = Join-Path $binariesDirectory "dpulse-backend-x86_64-pc-windows-msvc.exe"
New-Item -ItemType Directory -Force -Path $binariesDirectory | Out-Null
Copy-Item $builtBackend $sidecarPath -Force

Write-Host "Installing frontend dependencies..."
& npm install

Write-Host ""
Write-Host "Build completed successfully."
Write-Host "Sidecar: $sidecarPath"
Write-Host ""
Write-Host "Start development mode with:"
Write-Host "  npm run tauri dev"
Write-Host ""
Write-Host "Build an installer with:"
Write-Host "  npm run tauri build"

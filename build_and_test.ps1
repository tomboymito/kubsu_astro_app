# Config
$ProjectRoot = "C:\Users\maxvl\repos\kubsu_astro_app"
$BackendPath = "$ProjectRoot\backend"
$CppPath = "$BackendPath\cpp"
$PythonPath = "C:\Program Files\Python311\python.exe"

# 1. Setup virtual environment
Write-Host "[1/5] Setting up virtual environment..." -ForegroundColor Cyan
if (-not (Test-Path "$ProjectRoot\venv")) {
    & $PythonPath -m venv "$ProjectRoot\venv"
}
& "$ProjectRoot\venv\Scripts\Activate.ps1"

# 2. Install dependencies
Write-Host "[2/5] Installing Python dependencies..." -ForegroundColor Cyan
pip install -r "$BackendPath\requirements.txt"
pip install -e "$BackendPath"

# 3. Build C++ module
Write-Host "[3/5] Building C++ module..." -ForegroundColor Cyan
Set-Location "$CppPath"

# Clean previous build
if (Test-Path "build") {
    Remove-Item "build" -Recurse -Force
}
New-Item -ItemType Directory -Path "build" | Out-Null
Set-Location "build"

# Configure build
$CMakeArgs = @(
    "..",
    "-G `"Visual Studio 17 2022`"",
    "-A x64",
    "-DCMAKE_BUILD_TYPE=Release",
    "-Dpybind11_DIR=`"$CppPath\pybind11\share\cmake\pybind11`"",
    "-DPython3_ROOT_DIR=`"C:\Program Files\Python311`""
)

# Run CMake
& cmake $CMakeArgs
if ($LASTEXITCODE -ne 0) {
    Write-Host "CMake configuration failed!" -ForegroundColor Red
    exit 1
}

# Compile
& cmake --build . --config Release
if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed!" -ForegroundColor Red
    exit 1
}

# Verify output
$LibPath = "$BackendPath\app\core\calculations\comet_calculations.pyd"
if (-not (Test-Path $LibPath)) {
    Write-Host "Library not found at: $LibPath" -ForegroundColor Red
    exit 1
}

# 4. Run tests
Write-Host "[4/5] Running tests..." -ForegroundColor Cyan
Set-Location $BackendPath
$env:PYTHONPATH = "$BackendPath;$env:PYTHONPATH"

& pytest "tests/" -v
if ($LASTEXITCODE -ne 0) {
    Write-Host "Tests failed!" -ForegroundColor Red
    exit 1
}

# 5. Completion
Write-Host "[5/5] All checks completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "To start server run:" -ForegroundColor Yellow
Write-Host "  cd $BackendPath" -ForegroundColor Yellow
Write-Host "  uvicorn main:app --reload" -ForegroundColor Yellow
# PowerShell script to run backend and frontend concurrently with error handling
Start-Transcript -Path "logs/run_log.txt"
# run_all.ps1 - финальная версия с чистым выводом

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Создаем папку для логов
New-Item -ItemType Directory -Path logs -Force | Out-Null

Write-Host "=== Launching Application ==="

# Очистка порта
$processes = @(Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique)
if ($processes) {
    Write-Host "Found $($processes.Count) processes using port 8000:"
    $processes | ForEach-Object {
        $procName = (Get-Process -Id $_ -ErrorAction SilentlyContinue).ProcessName
        Write-Host " - Killing process $_ ($procName)"
        Stop-Process -Id $_ -Force
    }
    Start-Sleep -Seconds 2
}

# Запуск backend с логированием
Write-Host "Starting backend server (logs in logs/backend_*.log)..."
$backendJob = Start-Job -ScriptBlock {
    $env:PYTHONUNBUFFERED = "1"
    Set-Location $using:PWD
    & python -m uvicorn application.backend.main:app --port 8000 --host 0.0.0.0 1>logs/backend_out.log 2>logs/backend_error.log
}

# Ожидание с увеличенным таймаутом
Write-Host "Waiting for backend (20 sec max)..."
$attempts = 0
while ($attempts -lt 20) {
    $conn = Test-NetConnection -ComputerName localhost -Port 8000 -InformationLevel Quiet -WarningAction SilentlyContinue
    if ($conn) {
        Write-Host "Backend ready on port 8000"
        break
    }
    $attempts++
    Start-Sleep -Seconds 1
    
    # Вывод прогресса
    if ($attempts % 5 -eq 0) {
        Write-Host "Waiting... ($attempts/20 seconds passed)"
    }
}

if ($attempts -ge 20) {
    Write-Host "Backend failed to start after 20 seconds" -ForegroundColor Red
    Write-Host "Check logs/backend_error.log for details" -ForegroundColor Yellow
    exit 1
}

# Запуск frontend
Write-Host "Starting frontend application..."
try {
    $frontendProcess = Start-Process -NoNewWindow -PassThru -FilePath "python" -ArgumentList "application/frontend/front_v2.py"
    Wait-Process -Id $frontendProcess.Id
    Write-Host "Frontend closed"
} finally {
    Write-Host "Stopping backend..."
    Stop-Job $backendJob
    Remove-Job $backendJob
    Receive-Job $backendJob | Out-Null
}

Write-Host "=== Application stopped ==="

Stop-Transcript
# 1
Откройте PowerShell от имени администратора

# 2
Выполните команду:

```powershell
cd C:\Users\maxvl\repos\kubsu_astro_app
```

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
.\build_and_test.ps1
```

```powershell
cmake .. -G "Visual Studio 17 2022" -A x64 -DCMAKE_BUILD_TYPE=Release
cmake --build . --config Release
```

```
python.exe -m pip install --upgrade pip
```
## 1
```powershell
cd C:\Users\m8906\repos\kubsu_astro_app
```

## 2
```powershell
python -m venv venv
```

## 3
```powershell
python.exe -m pip install --upgrade pip
```

## 4
В корне проекта, также в app/backend и app/frontend
```powershell
pip install -r requirements.txt
```
## 5
```powershell
mkdir build
cd build
```
## 6
```powershell
cmake ..
cmake --build . --config Release
```

## 7
```powershell
powershell .\run_all.ps1
```
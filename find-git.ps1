dir "C:\Program Files\Git\cmd\git.exe" 2>$null
dir "C:\Program Files (x86)\Git\cmd\git.exe" 2>$null
dir "$env:LOCALAPPDATA\Microsoft\WindowsApps\git.exe" 2>$null
Get-ChildItem -Path "C:\Program Files" -Filter "git.exe" -Recurse -ErrorAction SilentlyContinue 2>$null | Select-Object FullName
"---DONE---"
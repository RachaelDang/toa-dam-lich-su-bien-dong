@echo off
chcp 65001 >nul
cd /d "C:\Users\Administrator\Downloads\Toa Dam Lich Su Bien Dong"

echo [1/3] Dang stage tat ca...
"C:\Program Files\Git\cmd\git.exe" add .
echo.

echo [2/3] Dang commit...
"C:\Program Files\Git\cmd\git.exe" commit -m "Cap nhat .gitignore, xoa file tam"
echo.

echo [3/3] Dang push...
"C:\Program Files\Git\cmd\git.exe" push origin main
echo.

echo === HOAN TAT ===
pause
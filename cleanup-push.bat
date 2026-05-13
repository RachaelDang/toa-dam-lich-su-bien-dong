@echo off
chcp 65001 >nul
cd /d "C:\Users\Administrator\Downloads\Toa Dam Lich Su Bien Dong"

echo [1/3] Dang xoa file push-update.bat ...
del /f push-update.bat 2>nul
echo [1.5] Dang xoa file push.bat ...
del /f push.bat 2>nul
echo [2/3] Dang stage tat ca...
"C:\Program Files\Git\cmd\git.exe" add . -A
echo [3/3] Dang commit va push...
"C:\Program Files\Git\cmd\git.exe" commit -m "Xoa file bat tam thoi, don dep repo"
"C:\Program Files\Git\cmd\git.exe" push origin main
echo.
echo === DONE ===
echo Website: https://RachaelDang.github.io/toa-dam-lich-su-bien-dong/
pause
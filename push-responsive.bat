@echo off
chcp 65001 >nul
cd /d "C:\Users\Administrator\Downloads\Toa Dam Lich Su Bien Dong"

echo [1/3] Stage tat ca...
"C:\Program Files\Git\cmd\git.exe" add . -A
echo.

echo [2/3] Commit...
"C:\Program Files\Git\cmd\git.exe" commit -m "Fix responsive mobile: background, image size, grid, nav"
echo.

echo [3/3] Push...
"C:\Program Files\Git\cmd\git.exe" push origin main
echo.
echo === DONE ===
echo Website: https://RachaelDang.github.io/toa-dam-lich-su-bien-dong/
pause
@echo off
cd /d "C:\Users\Administrator\Downloads\Toa Dam Lich Su Bien Dong"
"C:\Program Files\Git\cmd\git.exe" branch -M main
del /f install-git.ps1 find-git.ps1 setup-git.ps1
"C:\Program Files\Git\cmd\git.exe" add .
"C:\Program Files\Git\cmd\git.exe" commit -m "Initial commit: Toa Dam Lich Su Bien Dong"
echo Done!
echo.
echo === BUOC TIEP THEO ===
echo 1. Tao repo moi tren GitHub: https://github.com/new
echo 2. Chay cac lenh nay:
echo    git remote add origin https://github.com/USERNAME/toa-dam-lich-su-bien-dong.git
echo    git push -u origin main
echo 3. Vao repo Settings ^> Pages ^> Source: main branch /root
echo 4. Website: https://USERNAME.github.io/toa-dam-lich-su-bien-dong/
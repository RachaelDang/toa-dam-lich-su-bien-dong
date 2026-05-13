$ErrorActionPreference = "Continue"
$gitPath = "C:\Program Files\Git\cmd\git.exe"

Write-Host "=== Khoi tao Git repo ===" -ForegroundColor Cyan

cd "C:\Users\Administrator\Downloads\Toa Dam Lich Su Bien Dong"

# Kiem tra Git
& $gitPath --version

# Cau hinh Git neu chua co
$gitName = & $gitPath config --global user.name 2>$null
if (-not $gitName) {
    & $gitPath config --global user.name "KND Team"
    & $gitPath config --global user.email "knd@example.com"
    Write-Host "Da cau hinh Git" -ForegroundColor Green
}

# Khoi tao repo neu chua co
if (-not (Test-Path ".git")) {
    & $gitPath init
    Write-Host "Da khoi tao repo moi" -ForegroundColor Green
}

& $gitPath add .
& $gitPath commit -m "Initial commit: Toa Dam Lich Su Bien Dong"
Write-Host "Da commit!" -ForegroundColor Green

Write-Host ""
Write-Host "=== CAI DAT TAI GITHUB ===" -ForegroundColor Yellow
Write-Host "1. Vao https://github.com -> New repository" -ForegroundColor White
Write-Host "2. Dat ten: toa-dam-lich-su-bien-dong" -ForegroundColor White
Write-Host "3. KHONG tao README/ .gitignore (da co roi)" -ForegroundColor White
Write-Host "4. Sao chep 4 lenh duoi day:" -ForegroundColor White
Write-Host ""
Write-Host '  git remote add origin https://github.com/<USERNAME>/toa-dam-lich-su-bien-dong.git' -ForegroundColor Cyan
Write-Host '  git branch -M main' -ForegroundColor Cyan
Write-Host '  git push -u origin main' -ForegroundColor Cyan
Write-Host ""
Write-Host "=== DEPLOY ===" -ForegroundColor Yellow
Write-Host "Sau khi push, vao: Settings > Pages > Source: main branch / (root)" -ForegroundColor White
Write-Host "Website se o: https://<USERNAME>.github.io/toa-dam-lich-su-bien-dong/" -ForegroundColor Cyan
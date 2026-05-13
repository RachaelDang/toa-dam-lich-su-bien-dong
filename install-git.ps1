$ErrorActionPreference = "Continue"

# Install Git
Write-Host "=== Installing Git ===" -ForegroundColor Cyan
winget install --id Git.Git --accept-package-agreements --accept-source-agreements

# Install GitHub CLI
Write-Host "=== Installing GitHub CLI ===" -ForegroundColor Cyan
winget install --id GitHub.cli --accept-package-agreements --accept-source-agreements

Write-Host "=== Done ===" -ForegroundColor Green
RefreshEnv

# Verify
git --version
gh --version
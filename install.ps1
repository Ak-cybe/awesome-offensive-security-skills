# ============================================================================
# 🔥 CyberSkills Elite — Windows PowerShell Installer
# The World's Most Complete Offensive Security Skills for AI Agents
# ============================================================================

$ErrorActionPreference = "Stop"

$REPO_URL = "https://github.com/Ak-cybe/awesome-offensive-security-skills.git"
$REPO_DIR = "awesome-offensive-security-skills"
$VERSION = "1.0.0"

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Red
Write-Host "║     🔥 Awesome Offensive Security Skills — Installer v$VERSION  ║" -ForegroundColor Red
Write-Host "║    191 Offensive Security Skills for AI Coding Agents        ║" -ForegroundColor Red
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Red
Write-Host ""

# ─── Detect Agent ────────────────────────────────────────────────────────────
$AGENT = ""
$SKILL_DIR = ""

if (Get-Command claude -ErrorAction SilentlyContinue) {
    Write-Host "✓ Claude Code CLI detected" -ForegroundColor Green
    $AGENT = "claude"
    $SKILL_DIR = "$env:USERPROFILE\.claude\skills\cyberskills-elite"
}
elseif (Get-Command gemini -ErrorAction SilentlyContinue) {
    Write-Host "✓ Gemini CLI detected" -ForegroundColor Green
    $AGENT = "gemini"
    $SKILL_DIR = "$env:USERPROFILE\.gemini\skills\cyberskills-elite"
}
elseif (Get-Command cursor -ErrorAction SilentlyContinue) {
    Write-Host "✓ Cursor detected" -ForegroundColor Green
    $AGENT = "cursor"
    $SKILL_DIR = "$env:USERPROFILE\.cursor\skills\cyberskills-elite"
}
else {
    Write-Host "⚠  No AI agent CLI detected. Installing to current directory." -ForegroundColor Yellow
    $SKILL_DIR = ".\cyberskills-elite"
}

Write-Host "📁 Install location: $SKILL_DIR" -ForegroundColor Cyan
Write-Host ""

# ─── Clone or Update ─────────────────────────────────────────────────────────
if (Test-Path $REPO_DIR) {
    Write-Host "📥 Updating existing clone..." -ForegroundColor Cyan
    Push-Location $REPO_DIR
    git pull --quiet
    Pop-Location
}
else {
    Write-Host "📥 Cloning repository..." -ForegroundColor Cyan
    git clone --quiet --depth 1 $REPO_URL $REPO_DIR
}

# ─── Install ─────────────────────────────────────────────────────────────────
if (-not (Test-Path $SKILL_DIR)) {
    New-Item -ItemType Directory -Path $SKILL_DIR -Force | Out-Null
}

Write-Host "📦 Installing all skills..." -ForegroundColor Cyan
Copy-Item -Path "$REPO_DIR\skills\*" -Destination $SKILL_DIR -Recurse -Force

# ─── Summary ─────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                    ✅ Installation Complete                  ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "  Skills installed:  191" -ForegroundColor White
Write-Host "  Location:         $SKILL_DIR" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Quick Test — open your agent and try:" -ForegroundColor Magenta
Write-Host ""
Write-Host '  "Test this JWT for algorithm confusion attacks"' -ForegroundColor Cyan
Write-Host '  "Perform Kerberoasting on the domain controller"' -ForegroundColor Cyan
Write-Host '  "Test this chatbot for prompt injection bypasses"' -ForegroundColor Cyan
Write-Host ""
Write-Host "📖 Full catalog: https://github.com/Ak-cybe/awesome-offensive-security-skills" -ForegroundColor Yellow
Write-Host "⭐ Star the repo if it helps your security work!" -ForegroundColor Yellow
Write-Host ""

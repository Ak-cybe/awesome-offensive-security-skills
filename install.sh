#!/bin/bash
# ============================================================================
# 🔥 CyberSkills Elite — One-Command Installer
# The World's Most Complete Offensive Security Skills for AI Agents
# ============================================================================

set -e

REPO_URL="https://github.com/Ak-cybe/awesome-offensive-security-skills.git"
REPO_DIR="awesome-offensive-security-skills"
VERSION="1.0.0"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo ""
echo -e "${RED}${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${RED}${BOLD}║     🔥 Awesome Offensive Security Skills — Installer v${VERSION}  ║${NC}"
echo -e "${RED}${BOLD}║      191 Offensive Security Skills for AI Coding Agents      ║${NC}"
echo -e "${RED}${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ─── Detect Agent ────────────────────────────────────────────────────────────
AGENT=""
SKILL_DIR=""

if command -v claude &> /dev/null; then
    echo -e "${GREEN}✓${NC} Claude Code CLI detected"
    AGENT="claude"
    SKILL_DIR="$HOME/.claude/skills/cyberskills-elite"
elif command -v gemini &> /dev/null; then
    echo -e "${GREEN}✓${NC} Gemini CLI detected"
    AGENT="gemini"
    SKILL_DIR="$HOME/.gemini/skills/cyberskills-elite"
elif command -v cursor &> /dev/null; then
    echo -e "${GREEN}✓${NC} Cursor detected"
    AGENT="cursor"
    SKILL_DIR="$HOME/.cursor/skills/cyberskills-elite"
elif command -v windsurf &> /dev/null; then
    echo -e "${GREEN}✓${NC} Windsurf detected"
    AGENT="windsurf"
    SKILL_DIR="$HOME/.windsurf/skills/cyberskills-elite"
else
    echo -e "${YELLOW}⚠${NC}  No AI agent CLI detected. Installing to current directory."
    SKILL_DIR="./cyberskills-elite"
fi

echo -e "${BLUE}📁 Install location:${NC} $SKILL_DIR"
echo ""

# ─── Parse Arguments ─────────────────────────────────────────────────────────
INSTALL_ALL=true
CATEGORIES=()

show_help() {
    echo -e "${BOLD}Usage:${NC}"
    echo "  ./install.sh                    Install all 191 skills"
    echo "  ./install.sh --category web     Install only web security skills"
    echo "  ./install.sh --category ai      Install only AI red teaming skills"
    echo "  ./install.sh --list             List available categories"
    echo ""
    echo -e "${BOLD}Categories:${NC}"
    echo "  web        Web Application Security (28 skills)"
    echo "  api        API Security (9 skills)"
    echo "  ai         AI Red Teaming (25 skills) — EXCLUSIVE"
    echo "  network    Network Penetration Testing (9 skills)"
    echo "  ad         Active Directory Attacks (6 skills)"
    echo "  cloud      Cloud Security (10 skills)"
    echo "  redteam    Red Teaming Operations (21 skills)"
    echo "  ir         Incident Response & Forensics (10 skills)"
    echo "  bugbounty  Bug Bounty Methodology (9 skills)"
    echo "  labs       PortSwigger Deep-Dive Labs (31 skills)"
    echo "  all        Everything (191 skills)"
}

CATEGORY_MAP_web="bug-hunting/web-vulnerabilities"
CATEGORY_MAP_api="bug-hunting/api-security"
CATEGORY_MAP_ai="ai-red-teaming"
CATEGORY_MAP_network="penetration-testing/network"
CATEGORY_MAP_ad="penetration-testing/active-directory"
CATEGORY_MAP_cloud="penetration-testing/cloud-security"
CATEGORY_MAP_redteam="red-teaming"
CATEGORY_MAP_ir="incident-response"
CATEGORY_MAP_bugbounty="bug-hunting/methodology"
CATEGORY_MAP_labs="bug-hunting/deep-dive-labs"

while [[ $# -gt 0 ]]; do
    case $1 in
        --category|-c)
            INSTALL_ALL=false
            CATEGORIES+=("$2")
            shift 2
            ;;
        --list|-l)
            show_help
            exit 0
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# ─── Clone or Update ─────────────────────────────────────────────────────────
if [ -d "$REPO_DIR" ]; then
    echo -e "${CYAN}📥 Updating existing clone...${NC}"
    cd "$REPO_DIR" && git pull --quiet && cd ..
else
    echo -e "${CYAN}📥 Cloning repository...${NC}"
    git clone --quiet --depth 1 "$REPO_URL" "$REPO_DIR"
fi

# ─── Install ─────────────────────────────────────────────────────────────────
mkdir -p "$SKILL_DIR"

SKILL_COUNT=0

if [ "$INSTALL_ALL" = true ]; then
    echo -e "${CYAN}📦 Installing all skills...${NC}"
    cp -r "$REPO_DIR/skills/"* "$SKILL_DIR/"
    SKILL_COUNT=191
else
    for cat in "${CATEGORIES[@]}"; do
        VAR_NAME="CATEGORY_MAP_${cat}"
        CAT_PATH="${!VAR_NAME}"

        if [ -z "$CAT_PATH" ]; then
            echo -e "${RED}✗ Unknown category: $cat${NC}"
            echo "  Run ./install.sh --list for available categories"
            continue
        fi

        SRC="$REPO_DIR/skills/$CAT_PATH"
        if [ -d "$SRC" ]; then
            DEST_DIR="$SKILL_DIR/$CAT_PATH"
            mkdir -p "$(dirname "$DEST_DIR")"
            cp -r "$SRC" "$DEST_DIR"
            COUNT=$(find "$SRC" -name "SKILL.md" | wc -l | tr -d ' ')
            SKILL_COUNT=$((SKILL_COUNT + COUNT))
            echo -e "${GREEN}  ✓${NC} Installed $cat ($COUNT skills)"
        else
            echo -e "${RED}  ✗${NC} Category path not found: $SRC"
        fi
    done
fi

# ─── Also install tools ──────────────────────────────────────────────────────
if [ -d "$REPO_DIR/tools" ]; then
    cp -r "$REPO_DIR/tools" "$SKILL_DIR/../cyberskills-tools" 2>/dev/null || true
fi

# ─── Summary ─────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}${BOLD}║                    ✅ Installation Complete                  ║${NC}"
echo -e "${GREEN}${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${BOLD}Skills installed:${NC}  $SKILL_COUNT"
echo -e "  ${BOLD}Location:${NC}         $SKILL_DIR"
echo ""
echo -e "${PURPLE}${BOLD}🚀 Quick Test — open your agent and try:${NC}"
echo ""
echo -e "  ${CYAN}\"Test this JWT for algorithm confusion attacks\"${NC}"
echo -e "  ${CYAN}\"Perform Kerberoasting on the domain controller\"${NC}"
echo -e "  ${CYAN}\"Test this chatbot for prompt injection bypasses\"${NC}"
echo ""
echo -e "${YELLOW}📖 Full catalog: https://github.com/Ak-cybe/awesome-offensive-security-skills${NC}"
echo -e "${YELLOW}⭐ Star the repo if it helps your security work!${NC}"
echo ""

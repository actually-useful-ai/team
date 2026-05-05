#!/usr/bin/env bash
# banner.sh — Display per-seat ASCII banners for the team council.
# Usage: bash scripts/banner.sh <SEAT> [subtitle]
# Requires: pyfiglet (pip3 install pyfiglet)
# Fallback: toilet -f future, then figlet -f small, then plain text

set -euo pipefail

NAME="${1:-TEAM}"
SUBTITLE="${2:-}"
RESET='\033[0m'

get_font() {
    case "$1" in
        EXECUTIVE)   echo "calvin_s" ;;
        EDITOR)      echo "pagga" ;;
        RECON)       echo "smbraille" ;;
        SCOUT)       echo "emboss2" ;;
        MARKETING)   echo "broadway_kb" ;;
        LEGAL)       echo "heart_right" ;;
        MANAGER)     echo "linux" ;;
        ARCHITECT)   echo "fourtops" ;;
        GREYBEARD)   echo "straight" ;;
        SAFETY)      echo "fourtops" ;;
        TESTER)      echo "smbraille" ;;
        BREAKER)     echo "broadway_kb" ;;
        CYNIC)       echo "eftiwater" ;;
        TEAM)        echo "calvin_s" ;;
        *)           echo "small" ;;
    esac
}

get_color() {
    case "$1" in
        EXECUTIVE)   echo '\033[1;33m' ;;  # bold yellow
        EDITOR)      echo '\033[1;36m' ;;  # bold cyan
        RECON)       echo '\033[1;34m' ;;  # bold blue
        SCOUT)       echo '\033[1;36m' ;;  # bold cyan
        MARKETING)   echo '\033[1;35m' ;;  # bold magenta
        LEGAL)       echo '\033[0;37m' ;;  # white
        MANAGER)     echo '\033[1;33m' ;;  # bold yellow
        ARCHITECT)   echo '\033[1;34m' ;;  # bold blue
        GREYBEARD)   echo '\033[0;37m' ;;  # white
        SAFETY)      echo '\033[1;32m' ;;  # bold green
        TESTER)      echo '\033[1;33m' ;;  # bold yellow
        BREAKER)     echo '\033[1;31m' ;;  # bold red
        CYNIC)       echo '\033[1;35m' ;;  # bold magenta
        TEAM)        echo '\033[1;33m' ;;  # bold yellow
        PHASE*)      echo '\033[1;37m' ;;  # bold white
        *)           echo '\033[0m' ;;
    esac
}

FONT=$(get_font "$NAME")
COLOR=$(get_color "$NAME")

if python3 -c "import pyfiglet" 2>/dev/null; then
    printf "${COLOR}"
    python3 -c "import pyfiglet; print(pyfiglet.figlet_format('$NAME', font='$FONT').rstrip())"
    printf "${RESET}"
elif command -v toilet &>/dev/null; then
    printf "${COLOR}"
    toilet -f future "$NAME"
    printf "${RESET}"
elif command -v figlet &>/dev/null; then
    printf "${COLOR}"
    figlet -f small "$NAME"
    printf "${RESET}"
else
    printf "${COLOR}═══ %s ═══${RESET}\n" "$NAME"
fi

if [[ -n "$SUBTITLE" ]]; then
    printf "${COLOR}  %s${RESET}\n" "$SUBTITLE"
fi

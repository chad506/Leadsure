#!/usr/bin/env bash
#
# One-command refresh of marcy/listings.js from a Redfin "Download All" export,
# then commit + push so leadsure.com/marcy updates.
#
#   scripts/refresh-marcy-listings.sh                 # newest export in the default folder
#   scripts/refresh-marcy-listings.sh path/to/redfin_*.csv
#   scripts/refresh-marcy-listings.sh --no-push       # regenerate only, don't commit/push
#
# To refresh: re-run Redfin's "Download All" (CSV is simplest — no extra deps),
# drop it in the folder below, and run this.
set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"
EXPORT_DIR="${MARCY_EXPORT_DIR:-/Users/chadfisher/Library/CloudStorage/Dropbox/AMBAUM MASTER FOLDER/Clients/Ambaum/Real Estate}"
VENV="/tmp/marcy-venv"

NOPUSH=0
if [ "${1:-}" = "--no-push" ]; then NOPUSH=1; shift; fi

SRC="${1:-}"
if [ -z "$SRC" ]; then
  SRC="$(ls -t "$EXPORT_DIR"/redfin_*.numbers "$EXPORT_DIR"/redfin_*.csv 2>/dev/null | head -1 || true)"
fi
if [ -z "$SRC" ] || [ ! -f "$SRC" ]; then
  echo "No Redfin export found. Pass a file path, or set MARCY_EXPORT_DIR." >&2
  exit 1
fi
echo "Source: $SRC"

# .numbers needs the numbers-parser package (in a venv); .csv needs nothing.
if [[ "$SRC" == *.numbers ]]; then
  [ -x "$VENV/bin/python" ] || python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q numbers-parser || { echo "pip install numbers-parser failed" >&2; exit 1; }
  PY="$VENV/bin/python"
else
  PY="python3"
fi

"$PY" "$REPO/scripts/parse-redfin.py" "$SRC" "$REPO/marcy/listings.js" || exit 1

cd "$REPO"
if git diff --quiet -- marcy/listings.js; then
  echo "marcy/listings.js unchanged — nothing to push."
  exit 0
fi
if [ "$NOPUSH" = "1" ]; then
  echo "Regenerated marcy/listings.js (--no-push: not committing)."
  exit 0
fi
git add marcy/listings.js
git commit -q -m "Marcy: refresh listings from Redfin export ($(date +%Y-%m-%d))"
git push origin main
echo "Pushed — leadsure.com/marcy updates in ~1 min."

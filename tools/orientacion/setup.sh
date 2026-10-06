#!/usr/bin/env bash
# Descarga Support Fins (printfins.com) en una versión fija. No necesita npm install:
# su línea de comandos corre con Node 20.10+ sin dependencias.
set -euo pipefail
cd "$(dirname "$0")"

FINS_REPO="https://github.com/gittrahan/support-fins.git"
FINS_COMMIT="42dfed35b2b39e183fa73eecdd64f3ba29188e93"
DEST="vendor/support-fins"

if [ ! -d "$DEST/.git" ]; then
  mkdir -p "$DEST"
  git -C "$DEST" init -q
  git -C "$DEST" remote add origin "$FINS_REPO"
fi
# El repo guarda modelos de prueba en Git LFS; no hacen falta.
GIT_LFS_SKIP_SMUDGE=1 git -C "$DEST" fetch -q --depth 1 origin "$FINS_COMMIT"
GIT_LFS_SKIP_SMUDGE=1 git -C "$DEST" checkout -q FETCH_HEAD
node "$DEST/plugins/cli/support-fins.js" --help > /dev/null
echo "Support Fins listo ($FINS_COMMIT)."

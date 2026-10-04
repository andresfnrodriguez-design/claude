#!/usr/bin/env bash
# Descarga el motor de BumpMesh en una versión fija e instala sus dependencias.
set -euo pipefail
cd "$(dirname "$0")"

BUMPMESH_REPO="https://github.com/CNCKitchen/stlTexturizer.git"
BUMPMESH_COMMIT="ee02c390484d7d47c9023470380cba9a58f88299"
DEST="vendor/stlTexturizer"

if [ ! -d "$DEST/.git" ]; then
  mkdir -p "$DEST"
  git -C "$DEST" init -q
  git -C "$DEST" remote add origin "$BUMPMESH_REPO"
fi
git -C "$DEST" fetch -q --depth 1 origin "$BUMPMESH_COMMIT"
git -C "$DEST" checkout -q FETCH_HEAD

npm install --no-audit --no-fund
echo "BumpMesh listo ($BUMPMESH_COMMIT)."

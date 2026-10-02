#!/usr/bin/env bash
set -euo pipefail

TARGET_SHA="f645750f8c0de86c87b9344efeee659c7e65bad4"
REPO="${GITHUB_REPOSITORY}"
ASSET_DIR="release-assets"

expected=(
  "alpha-linux-0.1.0a2-alpha-amd64.iso.part-01"
  "alpha-linux-0.1.0a2-alpha-amd64.iso.part-02"
  "alpha-linux-0.1.0a2-alpha-amd64.iso.part-03"
  "alpha-linux-0.1.0a2-alpha-amd64.iso.part-04"
  "alpha-linux-0.1.0a2-alpha-amd64.iso.parts.sha256"
  "alpha-linux-0.1.0a2-alpha-amd64.iso.parts.json"
  "REASSEMBLE-ISO.txt"
)

for f in "${expected[@]}"; do
  test -f "$ASSET_DIR/$f"
done

ls -lh "$ASSET_DIR"

gh release view v0.1.0a2 -R "$REPO" >/dev/null 2>&1 ||   gh release create v0.1.0a2 -R "$REPO" --target "$TARGET_SHA" --title "Alpha Linux v0.1.0a2" --prerelease

gh release edit v0.1.0a2 -R "$REPO" --target "$TARGET_SHA" --prerelease

gh release upload v0.1.0a2 -R "$REPO"   "$ASSET_DIR/alpha-linux-0.1.0a2-alpha-amd64.iso.part-01"   "$ASSET_DIR/alpha-linux-0.1.0a2-alpha-amd64.iso.part-02"   "$ASSET_DIR/alpha-linux-0.1.0a2-alpha-amd64.iso.part-03"   "$ASSET_DIR/alpha-linux-0.1.0a2-alpha-amd64.iso.part-04"   --clobber

gh release upload v0.1.0a2 -R "$REPO"   "$ASSET_DIR/alpha-linux-0.1.0a2-alpha-amd64.iso.parts.sha256"   "$ASSET_DIR/alpha-linux-0.1.0a2-alpha-amd64.iso.parts.json"   "$ASSET_DIR/REASSEMBLE-ISO.txt"   --clobber

gh release edit v0.1.0a2 -R "$REPO" --target "$TARGET_SHA" --draft=false --prerelease

echo "A2 release published against exact target $TARGET_SHA"

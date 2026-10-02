#!/usr/bin/env bash
set -euo pipefail

TARGET_SHA="${TARGET_SHA:?TARGET_SHA must be supplied by the verified publisher workflow}"
REPO="${GITHUB_REPOSITORY}"
ASSET_DIR="release-assets"
RELEASE_TAG="v0.1.0a2"
RELEASE_NOTES_FILE="${RELEASE_NOTES_FILE:-docs/releases/v0.1.0a2.md}"

test -s "$RELEASE_NOTES_FILE" || {
  echo "ERROR: release notes are missing or empty: $RELEASE_NOTES_FILE" >&2
  exit 1
}

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

CURRENT_TAG_SHA="$(gh api "/repos/$REPO/git/ref/tags/$RELEASE_TAG" --jq '.object.sha' 2>/dev/null || true)"
if [[ -n "$CURRENT_TAG_SHA" && "$CURRENT_TAG_SHA" != "$TARGET_SHA" ]]; then
  echo "Existing $RELEASE_TAG tag points to $CURRENT_TAG_SHA; deleting release+tag so it can be recreated at the exact target."
  gh release delete "$RELEASE_TAG" -R "$REPO" --cleanup-tag --yes
fi

if ! gh release view "$RELEASE_TAG" -R "$REPO" >/dev/null 2>&1; then
  gh release create "$RELEASE_TAG" -R "$REPO"     --target "$TARGET_SHA"     --title "Alpha Linux v0.1.0a2"     --notes-file "$RELEASE_NOTES_FILE"     --prerelease
else
  gh release edit "$RELEASE_TAG" -R "$REPO"     --target "$TARGET_SHA"     --title "Alpha Linux v0.1.0a2"     --notes-file "$RELEASE_NOTES_FILE"     --prerelease
fi

gh release upload "$RELEASE_TAG" -R "$REPO"   "$ASSET_DIR/alpha-linux-0.1.0a2-alpha-amd64.iso.part-01"   "$ASSET_DIR/alpha-linux-0.1.0a2-alpha-amd64.iso.part-02"   "$ASSET_DIR/alpha-linux-0.1.0a2-alpha-amd64.iso.part-03"   "$ASSET_DIR/alpha-linux-0.1.0a2-alpha-amd64.iso.part-04"   --clobber

gh release upload "$RELEASE_TAG" -R "$REPO"   "$ASSET_DIR/alpha-linux-0.1.0a2-alpha-amd64.iso.parts.sha256"   "$ASSET_DIR/alpha-linux-0.1.0a2-alpha-amd64.iso.parts.json"   "$ASSET_DIR/REASSEMBLE-ISO.txt"   --clobber

gh release edit "$RELEASE_TAG" -R "$REPO"   --target "$TARGET_SHA"   --title "Alpha Linux v0.1.0a2"   --notes-file "$RELEASE_NOTES_FILE"   --draft=false   --prerelease

echo "A2 release published against exact target $TARGET_SHA with release notes from $RELEASE_NOTES_FILE"

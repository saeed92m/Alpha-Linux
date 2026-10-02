#!/usr/bin/env bash
set -euo pipefail

TARGET_SHA="f645750f8c0de86c87b9344efeee659c7e65bad4"
REPO="${GITHUB_REPOSITORY}"

echo "A2 target commit: $TARGET_SHA"

OS_READY="$(gh api "/repos/$REPO/actions/runs?branch=main&per_page=100" --jq '.workflow_runs[] | select(.name=="Alpha OS Image Final" and .head_sha=="'"$TARGET_SHA"'") | select(.status=="completed" and .conclusion=="success") | .id' | head -n 1 || true)"
CI_READY="$(gh api "/repos/$REPO/actions/runs?branch=main&per_page=100" --jq '.workflow_runs[] | select(.name=="Alpha Linux CI/CD" and .head_sha=="'"$TARGET_SHA"'") | select(.status=="completed" and .conclusion=="success") | .id' | head -n 1 || true)"
test -n "$OS_READY"
test -n "$CI_READY"
echo "Verified dependency runs: OS=$OS_READY CI=$CI_READY"

RUN_ID=""
while IFS= read -r candidate; do
  [[ -z "$candidate" ]] && continue
  count="$(gh api "/repos/$REPO/actions/runs/$candidate/artifacts" --jq '.total_count' 2>/dev/null || echo 0)"
  if [[ "$count" -ge 6 ]]; then
    RUN_ID="$candidate"
    break
  fi
done < <(gh api "/repos/$REPO/actions/runs?branch=main&per_page=100" --jq '.workflow_runs[] | select(.name=="Alpha OS Image Final" and .event=="push" and .head_sha=="'"$TARGET_SHA"'") | select(.status=="completed" and .conclusion=="success") | .id')
test -n "$RUN_ID"
echo "Selected OS image run: $RUN_ID"

gh release view v0.1.0a2 -R "$REPO" >/dev/null 2>&1 ||   gh release create v0.1.0a2 -R "$REPO" --target "$TARGET_SHA" --title "Alpha Linux v0.1.0a2" --prerelease
gh release edit v0.1.0a2 -R "$REPO" --target "$TARGET_SHA" --prerelease

rm -rf release-assets .a2-artifact
mkdir -p release-assets .a2-artifact/extracted

artifacts=(
  "alpha-linux-0.1.0a2-alpha-amd64.iso.part-01"
  "alpha-linux-0.1.0a2-alpha-amd64.iso.part-02"
  "alpha-linux-0.1.0a2-alpha-amd64.iso.part-03"
  "alpha-linux-0.1.0a2-alpha-amd64.iso.part-04"
  "alpha-linux-0.1.0a2-alpha-amd64-release-metadata"
  "alpha-linux-0.1.0a2-alpha-amd64-evidence"
)

for artifact in "${artifacts[@]}"; do
  id="$(gh api "/repos/$REPO/actions/runs/$RUN_ID/artifacts" --paginate --jq '.artifacts[] | select(.name=="'"$artifact"'" and .expired==false) | .id' | head -n 1)"
  test -n "$id"
  rm -rf .a2-artifact/extracted
  mkdir -p .a2-artifact/extracted
  curl --fail --location --retry 5 --retry-delay 3     -H "Authorization: Bearer $GH_TOKEN"     -H "Accept: application/vnd.github+json"     "https://api.github.com/repos/$REPO/actions/artifacts/$id/zip"     --output .a2-artifact/artifact.zip
  python3 - .a2-artifact/artifact.zip <<'PY'
import sys, zipfile
from pathlib import Path
archive = Path(sys.argv[1])
out = Path(".a2-artifact/extracted")
with zipfile.ZipFile(archive) as z:
    bad = z.testzip()
    if bad:
        raise SystemExit(f"corrupt zip member: {bad}")
    for info in z.infolist():
        if info.is_dir():
            continue
        target = out / Path(info.filename).name
        with z.open(info) as src, target.open("wb") as dst:
            while True:
                chunk = src.read(16 * 1024 * 1024)
                if not chunk:
                    break
                dst.write(chunk)
for p in out.iterdir():
    if p.is_file():
        p.replace(Path("release-assets") / p.name)
PY
done

expected=(
  "alpha-linux-0.1.0a2-alpha-amd64.iso.part-01"
  "alpha-linux-0.1.0a2-alpha-amd64.iso.part-02"
  "alpha-linux-0.1.0a2-alpha-amd64.iso.part-03"
  "alpha-linux-0.1.0a2-alpha-amd64.iso.part-04"
  "alpha-linux-0.1.0a2-alpha-amd64.iso.parts.sha256"
  "alpha-linux-0.1.0a2-alpha-amd64.iso.parts.json"
  "REASSEMBLE-ISO.txt"
)
for f in "${expected[@]}"; do test -f "release-assets/$f"; done

gh release upload v0.1.0a2 -R "$REPO"   release-assets/alpha-linux-0.1.0a2-alpha-amd64.iso.part-01   release-assets/alpha-linux-0.1.0a2-alpha-amd64.iso.part-02   release-assets/alpha-linux-0.1.0a2-alpha-amd64.iso.part-03   release-assets/alpha-linux-0.1.0a2-alpha-amd64.iso.part-04   --clobber

gh release upload v0.1.0a2 -R "$REPO"   release-assets/alpha-linux-0.1.0a2-alpha-amd64.iso.parts.sha256   release-assets/alpha-linux-0.1.0a2-alpha-amd64.iso.parts.json   release-assets/REASSEMBLE-ISO.txt   --clobber

gh release edit v0.1.0a2 -R "$REPO" --target "$TARGET_SHA" --draft=false --prerelease

echo "A2 publication completed and bound to $TARGET_SHA"

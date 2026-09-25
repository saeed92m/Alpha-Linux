import json

from alpha_core.provenance import create_provenance, sha256_bytes, write_provenance


def test_sha256_bytes_is_deterministic():
    assert sha256_bytes(b"alpha") == sha256_bytes(b"alpha")
    assert sha256_bytes(b"alpha") != sha256_bytes(b"beta")


def test_provenance_contains_required_identity(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    (root / "tracked.txt").write_text("alpha", encoding="utf-8")
    artifact = root / "artifact.whl"
    artifact.write_bytes(b"artifact")

    import subprocess
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)

    record = create_provenance(
        root=root, artifact=artifact, artifact_id="alpha.whl", artifact_type="package",
        version="0.1.0", channel="nightly", source_commit="abc", build_id="run-1",
        builder_identity="ci", package_set="foundation", configuration_digest="cfg",
        dependency_inventory="none", test_evidence="unit",
    )
    assert record["artifact_digest"]
    assert record["source_tree_digest"]
    assert record["signature"] is None

    out = tmp_path / "provenance.json"
    write_provenance(record, out)
    loaded = json.loads(out.read_text(encoding="utf-8"))
    assert loaded["artifact_id"] == "alpha.whl"

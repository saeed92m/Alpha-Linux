import pytest

from alpha_core.manifest import ProjectManifest


def valid_manifest(**kwargs):
    values = dict(
        project_id="alpha.example", schema_version="1", toolchain="python3.11",
        environment="venv", inputs=("src",), outputs=("build",),
        resources={"cpu": "adaptive"}, platform="linux", recovery="git+backup",
    )
    values.update(kwargs)
    return ProjectManifest(**values)


def test_manifest_validates():
    valid_manifest().validate()


def test_manifest_rejects_empty_required_field():
    with pytest.raises(ValueError):
        valid_manifest(project_id="").validate()


def test_manifest_rejects_secret_field():
    with pytest.raises(ValueError):
        valid_manifest(resources={"api_key": "do-not-store"}).validate()

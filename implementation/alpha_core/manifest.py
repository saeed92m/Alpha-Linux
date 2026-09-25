from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

_SECRET_NAMES = frozenset(
    {"password", "token", "secret", "api_key", "private_key", "credential"}
)


def _check_secret_keys(resources: Mapping[str, object]) -> None:
    for key in resources:
        normalized = key.lower().replace("-", "_")
        if normalized in _SECRET_NAMES or any(part in normalized for part in _SECRET_NAMES):
            raise ValueError("manifest must not contain secret fields")


@dataclass(frozen=True)
class ProjectManifest:
    project_id: str
    schema_version: str
    toolchain: str
    environment: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    resources: Mapping[str, str]
    platform: str
    recovery: str

    def validate(self) -> None:
        required = {
            "project_id": self.project_id,
            "schema_version": self.schema_version,
            "toolchain": self.toolchain,
            "environment": self.environment,
            "platform": self.platform,
            "recovery": self.recovery,
        }
        if any(not isinstance(value, str) or not value.strip() for value in required.values()):
            raise ValueError("manifest contains an empty required field")
        if not isinstance(self.inputs, tuple) or not isinstance(self.outputs, tuple):
            raise TypeError("manifest inputs and outputs must be tuples")
        if not self.inputs or not self.outputs:
            raise ValueError("manifest must declare inputs and outputs")
        if any(not isinstance(item, str) or not item.strip() for item in (*self.inputs, *self.outputs)):
            raise ValueError("manifest inputs and outputs must be non-empty strings")
        if not isinstance(self.resources, Mapping):
            raise TypeError("manifest resources must be a mapping")
        if any(not isinstance(k, str) or not k.strip() for k in self.resources):
            raise ValueError("manifest resource keys must be non-empty strings")
        _check_secret_keys(self.resources)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ProjectManifest":
        if not isinstance(data, Mapping):
            raise TypeError("manifest root must be an object")
        allowed = {
            "project_id", "schema_version", "toolchain", "environment",
            "inputs", "outputs", "resources", "platform", "recovery",
        }
        unknown = set(data) - allowed
        if unknown:
            raise ValueError(f"manifest contains unknown fields: {sorted(unknown)}")
        required = allowed
        missing = required - set(data)
        if missing:
            raise ValueError(f"manifest is missing required fields: {sorted(missing)}")
        manifest = cls(
            project_id=data["project_id"],
            schema_version=data["schema_version"],
            toolchain=data["toolchain"],
            environment=data["environment"],
            inputs=tuple(data["inputs"]),
            outputs=tuple(data["outputs"]),
            resources=dict(data["resources"]),
            platform=data["platform"],
            recovery=data["recovery"],
        )
        manifest.validate()
        return manifest

    @classmethod
    def from_json(cls, text: str) -> "ProjectManifest":
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("manifest is not valid JSON") from exc
        return cls.from_dict(data)

    @classmethod
    def from_file(cls, path: str | Path) -> "ProjectManifest":
        return cls.from_json(Path(path).read_text(encoding="utf-8"))

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "project_id": self.project_id,
            "schema_version": self.schema_version,
            "toolchain": self.toolchain,
            "environment": self.environment,
            "inputs": list(self.inputs),
            "outputs": list(self.outputs),
            "resources": dict(self.resources),
            "platform": self.platform,
            "recovery": self.recovery,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n"

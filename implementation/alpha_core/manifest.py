from dataclasses import dataclass
from typing import Mapping


_SECRET_NAMES = frozenset(
    {"password", "token", "secret", "api_key", "private_key", "credential"}
)


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
        if not self.inputs or not self.outputs:
            raise ValueError("manifest must declare inputs and outputs")
        if any(not item.strip() for item in (*self.inputs, *self.outputs)):
            raise ValueError("manifest inputs and outputs must not be empty")
        if any(key.lower() in _SECRET_NAMES for key in self.resources):
            raise ValueError("manifest must not contain secret fields")

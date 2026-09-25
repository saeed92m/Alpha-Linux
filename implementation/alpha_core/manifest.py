from dataclasses import dataclass
from typing import Mapping


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
        if any(not value.strip() for value in required.values()):
            raise ValueError("manifest contains an empty required field")
        if not self.inputs or not self.outputs:
            raise ValueError("manifest must declare inputs and outputs")
        secret_names = {"password", "token", "secret", "api_key", "private_key"}
        if any(key.lower() in secret_names for key in self.resources):
            raise ValueError("manifest must not contain secret fields")

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
from typing import Mapping


_PACKAGE_ID = re.compile(r"^[a-z0-9][a-z0-9+._-]*$")


@dataclass(frozen=True)
class SoftwareCatalogEntry:
    package_id: str
    name: str
    version: str
    summary: str
    source: str = "local"

    def __post_init__(self) -> None:
        if not _PACKAGE_ID.fullmatch(self.package_id):
            raise ValueError("invalid package identifier")
        if not self.name.strip() or not self.version.strip():
            raise ValueError("name and version are required")
        if not self.summary.strip():
            raise ValueError("summary is required")


@dataclass(frozen=True)
class SoftwareCatalog:
    entries: tuple[SoftwareCatalogEntry, ...]

    def __post_init__(self) -> None:
        ids = [entry.package_id for entry in self.entries]
        if ids != sorted(ids):
            raise ValueError("catalog entries must be sorted by package_id")
        if len(ids) != len(set(ids)):
            raise ValueError("catalog package identifiers must be unique")

    def get(self, package_id: str) -> SoftwareCatalogEntry | None:
        return next((entry for entry in self.entries if entry.package_id == package_id), None)


@dataclass(frozen=True)
class SoftwareTransactionPlan:
    plan_id: str
    action: str
    package_ids: tuple[str, ...]
    requires_privilege: bool = True
    dry_run: bool = True


class SoftwareCatalogLoader:
    """Read-only loader for deterministic local JSON catalog manifests."""

    def __init__(self, root: Path) -> None:
        self._root = root

    def load(self) -> SoftwareCatalog:
        entries: list[SoftwareCatalogEntry] = []
        if not self._root.is_dir():
            return SoftwareCatalog(())

        for path in sorted(self._root.glob("*.json")):
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError):
                continue
            if not isinstance(raw, dict):
                continue
            try:
                entries.append(
                    SoftwareCatalogEntry(
                        package_id=str(raw["package_id"]),
                        name=str(raw["name"]),
                        version=str(raw["version"]),
                        summary=str(raw["summary"]),
                        source=str(raw.get("source", "local")),
                    )
                )
            except (KeyError, TypeError, ValueError):
                continue

        entries.sort(key=lambda entry: entry.package_id)
        deduplicated: dict[str, SoftwareCatalogEntry] = {}
        for entry in entries:
            deduplicated.setdefault(entry.package_id, entry)
        return SoftwareCatalog(tuple(deduplicated.values()))


class SoftwareTransactionPlanner:
    """Creates deterministic dry-run plans; it never changes host package state."""

    def plan(
        self,
        action: str,
        package_ids: tuple[str, ...],
        *,
        requires_privilege: bool = True,
    ) -> SoftwareTransactionPlan:
        if action not in {"install", "remove"}:
            raise ValueError("action must be install or remove")
        normalized = tuple(sorted(set(package_ids)))
        if not normalized or any(not _PACKAGE_ID.fullmatch(package_id) for package_id in normalized):
            raise ValueError("package_ids must contain valid non-empty identifiers")
        identity = hashlib.sha256(
            "\0".join((action, *normalized)).encode("utf-8")
        ).hexdigest()[:16]
        return SoftwareTransactionPlan(
            plan_id=f"software-{identity}",
            action=action,
            package_ids=normalized,
            requires_privilege=requires_privilege,
            dry_run=True,
        )


def catalog_as_mapping(catalog: SoftwareCatalog) -> Mapping[str, object]:
    return {
        "entries": tuple(
            {
                "package_id": entry.package_id,
                "name": entry.name,
                "version": entry.version,
                "summary": entry.summary,
                "source": entry.source,
            }
            for entry in catalog.entries
        )
    }

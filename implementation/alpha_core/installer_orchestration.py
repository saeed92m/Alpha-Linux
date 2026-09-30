from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from .installer_safety import (
    InstallerIntent,
    ProposedChange,
    StorageObservation,
    propose_changes,
)
from .installer_transaction import (
    CommandRunner,
    TransactionResult,
    execute_disposable_transaction,
)


class InstallerStage(str, Enum):
    INITIAL = "initial"
    INSPECTED = "inspected"
    PLANNED = "planned"
    CONFIRMED = "confirmed"
    COMMITTED = "committed"
    ROLLED_BACK = "rolled-back"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class InstallerSession:
    """Fail-closed orchestration boundary between discovery, safety and mutation.

    Discovery is deliberately supplied by the caller so privileged hardware
    probing remains outside the policy engine. Physical block devices are not
    executable through this release's disposable transaction boundary.
    """

    stage: InstallerStage = InstallerStage.INITIAL
    observation: StorageObservation | None = None
    plan: ProposedChange | None = None
    transaction: TransactionResult | None = None

    def inspect(self, observation: StorageObservation) -> "InstallerSession":
        return InstallerSession(
            stage=InstallerStage.INSPECTED,
            observation=observation,
        )

    def plan_install(self, intent: InstallerIntent) -> "InstallerSession":
        if self.observation is None:
            raise RuntimeError("storage inspection is required before planning")
        plan = propose_changes(self.observation, intent)
        stage = (
            InstallerStage.BLOCKED
            if plan.safety.value == "blocked"
            else InstallerStage.PLANNED
        )
        return InstallerSession(
            stage=stage,
            observation=self.observation,
            plan=plan,
        )

    def confirm(self) -> "InstallerSession":
        if self.plan is None:
            raise RuntimeError("installation plan is required before confirmation")
        if self.stage is InstallerStage.BLOCKED:
            raise ValueError("blocked installation plan cannot be confirmed")
        if not self.plan.requires_explicit_confirmation:
            raise ValueError("plan does not require explicit confirmation")
        return InstallerSession(
            stage=InstallerStage.CONFIRMED,
            observation=self.observation,
            plan=self.plan,
        )

    def execute(
        self,
        target: Path,
        *,
        runner: CommandRunner | None = None,
        fail_at: int | None = None,
    ) -> "InstallerSession":
        if self.plan is None or self.observation is None:
            raise RuntimeError("inspection and planning are required before execution")
        if self.stage is not InstallerStage.CONFIRMED:
            raise PermissionError("explicit confirmation is required before execution")

        result = execute_disposable_transaction(
            self.plan,
            target,
            confirmed=True,
            runner=runner,
            fail_at=fail_at,
        )
        stage = (
            InstallerStage.COMMITTED
            if result.committed
            else InstallerStage.ROLLED_BACK
        )
        return InstallerSession(
            stage=stage,
            observation=self.observation,
            plan=self.plan,
            transaction=result,
        )

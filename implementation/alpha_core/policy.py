from .models import ActionDecision, ActionRequest, PermissionLevel, RiskLevel


class PolicyEngine:
    """Authoritative authorization boundary; model output is never authorization."""

    def decide(self, request: ActionRequest, *, approved: bool = False) -> ActionDecision:
        if not request.action_id or not request.actor or not request.target:
            return ActionDecision(False, "missing action identity or target", "POL-IDENTITY-001")

        if request.permission in {
            PermissionLevel.RESTRICTED_ADMIN,
            PermissionLevel.EXECUTE_APPROVAL,
        }:
            if not request.capabilities:
                return ActionDecision(False, "required capability is missing", "POL-CAPABILITY-001")
            if not approved:
                return ActionDecision(
                    False,
                    "explicit approval required",
                    "POL-APPROVAL-001",
                    requires_approval=True,
                )

        if request.risk in {RiskLevel.HIGH, RiskLevel.CRITICAL} and not approved:
            return ActionDecision(
                False,
                "high-risk action requires explicit approval",
                "POL-RISK-001",
                requires_approval=True,
            )

        return ActionDecision(True, "authorized by policy", "POL-DEFAULT-001")

from .models import ActionDecision, ActionRequest, PermissionLevel


class PolicyEngine:
    """Non-model authorization boundary for Alpha actions."""

    def decide(self, request: ActionRequest, *, approved: bool = False) -> ActionDecision:
        if not request.action_id or not request.actor:
            return ActionDecision(False, "missing action identity", "POL-IDENTITY-001")

        if request.permission in {
            PermissionLevel.RESTRICTED_ADMIN,
            PermissionLevel.EXECUTE_APPROVAL,
        } and not approved:
            return ActionDecision(False, "explicit approval required", "POL-APPROVAL-001")

        return ActionDecision(True, "authorized by policy", "POL-DEFAULT-001")

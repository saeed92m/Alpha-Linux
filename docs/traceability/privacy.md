# Phase 6 Privacy Hardening Traceability

| Requirement | Implementation | Tests | Evidence |
| --- | --- | --- | --- |
| Data classification | PrivacyClassification | policy construction | Immutable enum |
| Purpose binding | PrivacyPurpose / PrivacyPolicy | purpose match | Deterministic policy evaluation |
| Consent requirement | PrivacyPolicy / PrivacyRequest | missing consent | Explicit deny |
| Retention | PrivacyPolicy / PrivacyRequest | expiry test | Explicit deny |
| Deny by default | PrivacyPlanner.evaluate | missing-purpose test | No matching policy => deny |
| Deterministic normalization | PrivacyPlanner.normalize | ordering test | Stable policy ID ordering |
| Bounded planning | PrivacyPlanner.plan | bound test | Explicit policy limit |
| Reference-only boundary | module/spec | suite | No side effects |

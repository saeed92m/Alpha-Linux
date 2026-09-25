# Alpha Linux — System Integration Architecture

**Status:** Phase 2 implementation architecture

The System Integration Layer sits above OS foundations and below user-facing Control Center/Observatory services.

```
Alpha Core
   |
System Integration
   +-- Configuration Store
   +-- System Discovery
   +-- Diagnostics
   +-- Package/Update Planner
   +-- Health Aggregator
   |
OS adapters / future privileged backends
```

## Boundaries

1. **Configuration Store** owns typed namespaced state, not secrets or authorization.
2. **System Discovery** is read-only and reports evidence.
3. **Diagnostics** converts observations into structured findings; it does not authorize remediation.
4. **Package/Update Planner** produces plans and transaction metadata; privileged package mutation remains outside this reference implementation.
5. **Health Aggregator** combines component health without granting authority.

All components are deterministic reference implementations first. Ubuntu/COSMIC adapters will be added behind these contracts.

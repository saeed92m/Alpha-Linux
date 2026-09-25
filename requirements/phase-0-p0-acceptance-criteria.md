# Alpha Linux — Phase 0 P0 Acceptance Criteria

**Status:** Normative verification baseline

A P0 requirement is accepted only when its stated behavior is demonstrated by the listed evidence type and the applicable architecture/security/recovery gates are satisfied.

| Requirement family | Acceptance condition | Minimum evidence |
|---|---|---|
| AL-REQ-0001 | Supported installation boots a coherent Alpha workstation using declared Ubuntu/COSMIC foundations without prohibited foundation replacement. | Boot/system validation |
| AL-REQ-0002 | Core management surfaces expose consistent configuration for declared supported workflows. | Integration test |
| AL-REQ-0003 | Core and optional capability sets can be installed/removed according to declared modularity boundaries without invalid dependency state. | Package/install test |
| AL-REQ-0004 | Supported interfaces and compatibility boundaries are documented and verified against the declared Ubuntu target. | Compatibility evidence |
| AL-AI-0001 | AI can complete explain/inspect/suggest/authorized execute/verify/report flows with visible state. | End-to-end agent test |
| AL-AI-0002 | Attempted unauthorized tool actions are denied by non-model enforcement. | Security test |
| AL-AI-0004 | User can see agent state, requested permission, action and verification result. | UX test |
| AL-AI-0005 | Memory, Learning and Training have separate user-visible controls and documented data boundaries. | Privacy/system test |
| AL-REQ-0010 | Hardware, firmware, network, power and diagnostics expose declared state and actionable failures. | System test |
| AL-REQ-0011 | A supported update creates a recovery point, performs health validation and can roll back a representative failed transaction. | Fault-injection test |
| AL-REQ-0012 | Supported installation/recovery scenarios complete without unsafe silent disk mutation and expose recovery on failure. | Installer/recovery test |
| AL-REQ-0021 | Domain integration cannot alter foundation policy without the defined architecture/change process. | Architecture/security test |
| AL-REQ-0022 | Proprietary software workflows do not redistribute unlicensed commercial software. | Compliance review |
| AL-NFR-0001 | Each declared artifact class meets its documented reproducibility target. | Reproducibility evidence |
| AL-NFR-0002 | Artifact maps to immutable source and recorded build metadata. | Provenance audit |
| AL-NFR-0003 | Critical failures provide actionable diagnostics and a documented recovery route. | Fault/UX test |
| AL-NFR-0004 | Critical workflows pass applicable accessibility checks. | Accessibility evidence |
| AL-NFR-0005 | Release compatibility claims have reproducible supporting evidence. | Compatibility audit |
| AL-NFR-0006 | Observability supports diagnostics while excluding unnecessary sensitive collection. | Privacy/security test |
| AL-NFR-0007 | Release channel and version semantics are machine- and documentation-consistent. | Release test |
| AL-NFR-0008 | Declared resource budgets are measured on representative device/workload classes. | Performance evidence |
| AL-NFR-0009 | Failure-prone operations reach documented deterministic or recovery states. | Fault-injection evidence |
| AL-NFR-0010 | Critical architecture records identify trust boundaries, dependencies and owners. | Architecture audit |
| AL-SEC-0001 | Privileged operations cannot execute outside applicable authorization boundaries. | Security test |
| AL-SEC-0002 | AI plans alone cannot authorize protected operations. | Security test |
| AL-SEC-0003 | Destructive/admin AI actions require applicable approval or a documented safe-policy exception. | Security/UX test |
| AL-SEC-0004 | Secret scanning and artifact inspection show no prohibited embedded secrets. | Security scan |
| AL-SEC-0005 | Release artifacts verify authenticated integrity according to channel policy. | Verification test |
| AL-SEC-0006 | Release build has a complete dependency/software inventory. | SBOM/provenance audit |
| AL-SEC-0007 | Plugin/agent capabilities are constrained by trust, permission and isolation policy. | Security test |
| AL-SEC-0008 | Privacy-sensitive collection is explicit, minimized and user-controllable. | Privacy audit |
| AL-SEC-0009 | Recovery cannot silently bypass authentication/encryption protections. | Recovery/security test |
| AL-SEC-0010 | Security-critical changes have recorded review before stable release. | Release audit |
| AL-COMP-0001 | Declared release passes validation across the supported Ubuntu 26.04 LTS point-release policy. | Compatibility matrix |
| AL-COMP-0003 | Tested hardware is assigned the correct support status with evidence. | Hardware matrix |
| AL-COMP-0004 | Dual-boot validation inspects UEFI/GPT/ESP/NTFS/BitLocker state before mutation. | Installer test |
| AL-COMP-0005 | WSL-specific behavior is tested separately from bare-metal semantics. | Integration test |
| AL-COMP-0006 | Unsupported configurations are never presented as validated support. | Documentation audit |
| AL-REC-0001 | Each documented recovery layer has a tested entry and expected outcome for applicable failure classes. | Recovery evidence |
| AL-REC-0002 | Supported transactional updates establish a recovery point before mutation. | Fault-injection test |
| AL-REC-0003 | Representative failed updates roll back to the last validated state. | Recovery test |
| AL-REC-0004 | Supported boot failures can reach the documented boot-repair workflow. | Boot test |
| AL-REC-0005 | Emergency diagnostic access is available when the normal desktop is unavailable. | Recovery test |
| AL-REC-0006 | Representative failure scenarios are executed and retained as evidence. | QA report |
| AL-BLD-0001 | Every artifact records immutable source identity. | Provenance |
| AL-BLD-0002 | Build inputs/toolchain/package/configuration are recorded. | Provenance |
| AL-BLD-0003 | Required CI gates execute and failures block applicable promotion. | CI evidence |
| AL-BLD-0004 | Artifact digest and required signatures verify successfully. | Release verification |
| AL-BLD-0005 | ISO boot/live/install validation passes for the declared release scope. | ISO QA |
| AL-BLD-0006 | Package promotion follows candidate → validation → signed stable flow. | Repository evidence |
| AL-REL-0001 | Release channels and version semantics are consistent across metadata and documentation. | Release audit |
| AL-REL-0002 | Stable release contains notes, known issues, compatibility and verification instructions. | Release checklist |
| AL-REL-0003 | Provenance remains retrievable for the declared retention lifecycle. | Audit |
| AL-HW-0001 | Supported hardware classes are detected and classified correctly. | Hardware test |
| AL-HW-0003 | Compatibility status taxonomy is correctly applied. | Compatibility test |
| AL-HW-0004 | Risky hardware-management failure paths are recoverable. | Fault/recovery test |
| AL-UX-0001 | Critical workflows are keyboard/pointer operable. | Accessibility test |
| AL-UX-0003 | Critical workflows remain usable at supported HiDPI/mixed-DPI configurations. | UI test |
| AL-UX-0004 | Theme modes use semantic tokens without uncontrolled hard-coded colors. | UI inspection |
| AL-UX-0005 | AI state/permission/progress/action/verification are visible. | UX test |
| AL-UX-0006 | Applicable accessibility checks pass. | Accessibility audit |
| AL-PKG-0001 | Package origin is inspectable. | Package audit |
| AL-PKG-0002 | Repository policy rejects uncontrolled incompatible mixing. | Configuration test |
| AL-PKG-0003 | Alpha packages cannot reach stable without required gates. | CI/repository test |
| AL-PKG-0004 | Repository metadata/package integrity verifies according to channel policy. | Security test |
| AL-TEST-0001 | Traceability audit finds verification methods for every P0 requirement. | Traceability report |
| AL-TEST-0002 | Applicable stable-release validation gates have passed. | Release evidence |
| AL-TEST-0003 | Critical recovery paths have been exercised. | Fault-injection report |
| AL-TEST-0004 | Evidence identifies artifact, version, environment, result and timestamp. | Evidence audit |
| AL-TEST-0005 | Release-critical failures block stable promotion unless formally dispositioned. | Release-gate evidence |

## Gate

Any P0 requirement without a satisfied acceptance condition remains **not ready** for stable implementation/release.

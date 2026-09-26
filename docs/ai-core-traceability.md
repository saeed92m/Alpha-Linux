# Alpha AI Core Traceability

| Contract requirement | Implementation | Test evidence |
|---|---|---|
| Immutable model/provider contract | ModelDescriptor | descriptor validation tests |
| Deterministic registry | AICorePlanner.normalize / AIRegistry | test_registry_normalization_is_deterministic |
| Unique model IDs | AIRegistry | test_duplicate_model_ids_are_rejected |
| Model selection validation | AICorePlanner.select_model | test_unknown_model_selection_is_rejected |
| Request validation | AICorePlanner.validate_request | test_request_validates_against_registry |
| Capability invariants | ModelDescriptor | test_capabilities_are_deterministic_and_unique |

## Security trace

The implementation is declarative and side-effect free. It has no provider credentials, network execution, arbitrary command execution, autonomous actions, or host mutation capability. Production execution remains behind explicit service, authorization, and verification boundaries.

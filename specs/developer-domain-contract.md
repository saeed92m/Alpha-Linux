# Alpha Developer Domain Contract

The Developer domain is the first Phase 5 reference foundation.

## Responsibilities
- Represent immutable developer workspaces and toolchain capabilities.
- Normalize toolchains deterministically.
- Select enabled toolchains compatible with all workspace languages.
- Bound the number of selected toolchains.

## Invariants
- Workspace and toolchain identifiers are non-empty.
- Workspace and toolchain language sets are non-empty and unique.
- Disabled toolchains are never selected.
- A toolchain must support every requested workspace language.
- Toolchain selection is deterministic and bounded.

## Security boundary

This foundation performs no package installation, subprocess execution, filesystem mutation, network access, credential handling, or host mutation.

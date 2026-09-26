# Creator Traceability

| Requirement | Implementation | Tests | Boundary |
| --- | --- | --- | --- |
| Immutable creator project contract | CreatorProject | project validation | Pure contract |
| Explicit asset lifecycle role | CreatorAssetRole / CreatorAsset | asset-role and validation tests | No asset mutation |
| Source/proxy/cache/output separation | CreatorProject.assets | asset scope and plan tests | No deletion or replacement |
| Immutable creator tool contract | CreatorTool | tool validation | No tool execution |
| Explicit production requirement | CreatorRequirement | requirement validation | Pure contract |
| Deterministic asset normalization | normalize_assets | normalization test | Pure transformation |
| Deterministic tool normalization | normalize_tools | normalization test | Pure transformation |
| Media-kind compatibility | CreatorPlanner.plan | media-kind tests | No media processing |
| Capability compatibility | CreatorPlanner.plan | capability test | No tool execution |
| Bounded tool planning | max_tools | tool-limit test | No host mutation |
| Explicit rejection semantics | value objects and planner | rejection tests | No network, subprocess, or credentials |

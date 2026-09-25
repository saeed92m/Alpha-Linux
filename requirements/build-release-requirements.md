# Alpha Linux — Build and Release Requirements

| ID | Requirement | Validation |
|---|---|---|
| AL-BLD-0001 | Every release artifact shall be associated with an immutable source commit or equivalent immutable source identity. | Release audit |
| AL-BLD-0002 | Build inputs, toolchain, package set and relevant configuration shall be recorded for release artifacts. | Provenance audit |
| AL-BLD-0003 | CI shall execute required quality and security gates before merge or release promotion. | CI test |
| AL-BLD-0004 | Release artifacts shall have checksums and authenticated signatures when the release channel requires them. | Release test |
| AL-BLD-0005 | ISO artifacts shall undergo boot, live-session and installation validation before stable publication. | System test |
| AL-BLD-0006 | Package repositories shall promote artifacts through controlled candidate and stable stages. | Repository test |
| AL-REL-0001 | Alpha shall use explicit release channels and semantic versioning policy. | Release audit |
| AL-REL-0002 | Stable releases shall publish release notes, known issues, compatibility information and verification instructions. | Release checklist |
| AL-REL-0003 | Release provenance shall be retained for the defined lifecycle of the release. | Audit |

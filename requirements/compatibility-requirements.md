# Alpha Linux — Compatibility Requirements

| ID | Requirement | Validation |
|---|---|---|
| AL-COMP-0001 | Alpha shall target supported Ubuntu 26.04 LTS point releases rather than binding the product to a single initial point-release snapshot. | Release validation |
| AL-COMP-0002 | Alpha shall maintain a documented compatibility matrix for supported hardware classes. | Compatibility audit |
| AL-COMP-0003 | Alpha shall distinguish Working, Working with limitations, Driver required, Unsupported and Not tested hardware states. | Hardware test |
| AL-COMP-0004 | Dual-boot support shall account for UEFI/GPT, ESP, NTFS and BitLocker-related states before disk mutation. | Installer test |
| AL-COMP-0005 | WSL integration shall document differences between WSL and bare-metal Linux semantics. | Integration test |
| AL-COMP-0006 | Unsupported configurations shall be clearly identified rather than represented as validated support. | Documentation audit |

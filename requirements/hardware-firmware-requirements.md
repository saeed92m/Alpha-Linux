# Alpha Linux — Hardware and Firmware Requirements

| ID | Requirement | Priority | Validation |
|---|---|---|---|
| AL-HW-0001 | Alpha shall detect and classify supported CPU, GPU, memory, storage, network, input, display and power hardware. | P0 | Hardware test |
| AL-HW-0002 | Alpha shall expose firmware status for supported firmware-managed devices and distinguish available, current, failed and unsupported operations. | P1 | Firmware test |
| AL-HW-0003 | Hardware compatibility status shall distinguish Working, Limited, Driver Required, Unsupported and Not Tested. | P0 | Compatibility test |
| AL-HW-0004 | Hardware-management actions shall provide a safe failure and recovery path where the operation can affect boot, firmware or persistent configuration. | P0 | Fault-injection/recovery test |

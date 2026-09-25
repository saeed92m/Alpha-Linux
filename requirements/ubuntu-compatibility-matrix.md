# Ubuntu Compatibility Matrix

This matrix is a release-critical control.

| Capability | Alpha policy | Validation |
|---|---|---|
| APT | Preserve and integrate | Automated + system |
| Ubuntu repositories | Preserve compatibility | Repository tests |
| .deb packages | Preserve compatibility | Package tests |
| Snap ecosystem | Preserve unless explicitly documented | Integration tests |
| Kernel support | Preserve Ubuntu-supported baseline | Hardware matrix |
| Drivers/firmware | Preserve supported ecosystem | Hardware validation |
| Networking | Preserve | System tests |
| Bluetooth | Preserve | Hardware tests |
| Printing/scanning | Preserve | Device tests |
| Accessibility | Preserve and extend | Accessibility tests |
| Virtualization | Preserve supported foundations | Integration tests |
| Security services | Preserve and harden | Security tests |

Any intentional incompatibility must be documented, justified, tested and visible in release notes.

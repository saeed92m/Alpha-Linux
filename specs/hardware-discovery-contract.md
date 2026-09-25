# Hardware Discovery Contract

## Purpose

Hardware Discovery exposes read-only, structured host evidence to Alpha services, Control Center, diagnostics, and AI consumers.

## Current evidence

The reference implementation may expose:

- CPU architecture and logical CPU count.
- Memory totals from /proc/meminfo.
- DMI vendor/product/board fields from /sys/class/dmi/id.
- Battery state from /sys/class/power_supply.

## Safety

- Discovery is read-only.
- No shell commands are required.
- Missing or inaccessible files produce degraded evidence rather than fabricated values.
- Discovery does not authorize hardware or firmware mutation.
- Secrets and credentials are outside the discovery contract.

## Extension boundary

Future GPU, PCI, USB, firmware, thermal, storage, display, audio, network, and sensor adapters must preserve the same read-only and privacy boundaries and provide explicit evidence provenance.

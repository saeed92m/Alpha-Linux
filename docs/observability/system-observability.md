# Alpha System Observability

Alpha must make system state inspectable without requiring users to manually reconstruct it from unrelated tools.

## Domains

- CPU/GPU;
- RAM/VRAM;
- storage/I/O;
- network;
- thermals;
- power/battery;
- processes/services;
- containers/VMs;
- background tasks;
- AI agents and tool activity.

## Diagnostics flow

```
Detect
→ Collect Evidence
→ Correlate
→ Explain
→ Recommend
→ Apply (if authorized)
→ Verify
```

Observability must preserve privacy and minimize collection of unnecessary sensitive data.

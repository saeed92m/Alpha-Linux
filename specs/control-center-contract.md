# Control Center Backend Contract

Control Center aggregates System Observatory, Hardware Discovery and Update
Engine state for future COSMIC UI consumers.

It is an aggregation facade, not an authorization boundary. It may prepare an
update request, but execution remains subject to the Update Engine and the
existing policy/SystemService boundary.

Read-only state is exposed as immutable dataclasses. Future privileged
operations must preserve the same policy, audit, verification and recovery
boundaries.

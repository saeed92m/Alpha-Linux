# Alpha Linux Master Handbook

## Purpose

The Master Handbook is the learning and operational guide for understanding Alpha Linux from first principles through distribution engineering, AI integration, implementation, testing, release engineering and maintenance.

It is deliberately separate from the normative specification.

## Learning path

1. Computer and operating-system fundamentals
2. Linux fundamentals
3. Ubuntu/Debian foundation
4. Kernel, boot, storage, memory and services
5. Hardware, drivers, networking and security
6. Desktop Linux and COSMIC
7. Distribution engineering
8. Bootable media and Live environments
9. Installation, partitioning, boot configuration and recovery
10. Alpha architecture
11. AI, LLMs, memory and agents
12. Alpha implementation
13. Testing and QA
14. Release engineering
15. Maintenance and evolution

## Chapter method

Each chapter should contain:

- Concept
- Why it matters
- How Linux/Ubuntu implements it
- How Alpha uses it
- Architecture
- Practical examples
- Tools and commands
- Configuration
- Common failures
- Troubleshooting
- Security considerations
- Alpha-specific decisions
- Testing
- Exercises

Each chapter should end with:

> بعد از این فصل باید چه چیزی بلد باشم؟

## Handbook vs specification

The Handbook teaches **what, why and how the underlying concepts work**.

The Specification defines **exactly what Alpha Linux must provide**.

The Architecture describes **how Alpha is intended to provide it**.

The Implementation is the actual system.

Testing demonstrates that the system satisfies its requirements.

## Current phase

The project is currently in **Phase 7 — Alpha releases**.

The verified baseline includes executable Alpha Core and reference-runtime foundations, deterministic package/OS-image evidence, the `v0.1.0a1` release, QEMU pre-install boot-smoke evidence, installer safety planning and executable disposable transaction validation.

The next release-scoped work extends this baseline into boot compatibility, Live environment validation, graphical installer architecture, transaction/recovery evidence and physical installation gates.

The Handbook remains educational and must not be treated as a substitute for normative requirements or architecture decisions.

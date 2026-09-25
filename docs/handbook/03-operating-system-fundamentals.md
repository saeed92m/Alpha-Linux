# Chapter 03 — Operating System Fundamentals

## Concept

An operating system coordinates hardware resources and provides stable abstractions to applications. In Alpha Linux, this includes the Linux kernel, system services, device interfaces, filesystems, networking, security controls and user-space services.

## Why it matters to Alpha

Alpha is not an operating-system foundation rewrite. Its product value is built by integrating and orchestrating established layers while keeping ownership boundaries explicit.

## Core model

```
Hardware
   ↓
Firmware / Boot
   ↓
Linux Kernel
   ↓
systemd + drivers + core user space
   ↓
Ubuntu platform
   ↓
COSMIC + Alpha system services
   ↓
Alpha AI / tools / domains
```

The upper layers depend on contracts exposed by lower layers. A user-facing feature must not become a reason to bypass kernel, security or package-management invariants.

## Key concepts

### Kernel

The kernel manages CPU scheduling, memory, processes, devices, networking primitives and security mechanisms. Alpha normally consumes these interfaces rather than replacing them.

### Processes and services

A process is an executing program. A service is a long-running system component managed through an appropriate service mechanism. Alpha services must have explicit privileges, dependencies, startup/shutdown behavior and failure handling.

### Filesystems and storage

Applications see filesystem abstractions rather than raw storage devices. Storage operations that can destroy or alter persistent state require explicit scope and recovery handling.

### Security boundary

Authentication establishes identity; authorization determines permitted actions. Alpha must preserve this distinction. An AI plan is a request, not authorization.

### User space

Most Alpha functionality belongs in user space. This keeps iteration safer and makes Ubuntu compatibility easier while allowing Alpha to provide system integration services.

## Alpha design rule

**Own the experience, integrate the ecosystem, don't reinvent the foundation.**

This principle does not prohibit lower-level changes when required; it requires a documented architecture decision demonstrating why an upstream or existing interface is insufficient.

## Practical inspection

Typical Linux investigation tools include:

- `uname`, `lsb_release` or OS-release metadata
- `systemctl`
- `journalctl`
- `ps`, `top` and resource monitors
- `lsblk`, `findmnt`, filesystem tools
- `ip`, NetworkManager tooling
- `lspci`, `lsusb`, `udevadm`

Commands are examples for learning; production Alpha tooling should provide safer structured interfaces and actionable diagnostics.

## Failure thinking

For every system operation ask:

1. What state changes?
2. Which privilege is required?
3. What can fail?
4. What evidence is generated?
5. How is the operation reversed or recovered?

## After this chapter

You should be able to explain the relationship between hardware, firmware, kernel, system services, Ubuntu, COSMIC and Alpha, and identify where a proposed feature belongs in that stack.

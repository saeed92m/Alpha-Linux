# Ubuntu and Debian Foundation

## Concept

Alpha Linux is built on Ubuntu 26.04 LTS and deliberately uses the Ubuntu foundation rather than replacing the distribution substrate.

Ubuntu supplies the kernel packaging model, base system, package ecosystem, security updates, hardware enablement and long-established operational interfaces. Alpha owns the product experience, integration layer, AI-native services, policy orchestration, domain platform and user-facing tooling.

## Why this boundary matters

Alpha is Ubuntu-compatible by design, not Ubuntu-limited by design.

The foundation boundary prevents unnecessary divergence while allowing Alpha to add value above the operating-system substrate.

## Package and repository discipline

Alpha MUST prefer:
1. official Ubuntu repositories for Ubuntu-provided components;
2. explicitly controlled upstream ecosystems where approved;
3. vendor-controlled installation paths for proprietary applications.

Uncontrolled mixing of arbitrary Debian or third-party repositories is prohibited.

## Alpha boundary

The intended layering is:

```
Ubuntu foundation
    ↓
Alpha System Services
    ↓
Alpha Experience
    ↓
Alpha Intelligence
    ↓
Alpha Platform / Domain Suites
```

A higher layer MUST NOT silently redefine security, recovery, packaging or boot behavior owned by a lower authoritative layer.

## Practical engineering rule

When implementing a feature, first determine whether Ubuntu already provides the primitive. If it does, integrate it through a documented interface instead of rebuilding it.

## Failure handling

A failure in Alpha services must not make the underlying Ubuntu recovery path unusable.

## Exercises

- Identify which parts of a proposed feature belong to Ubuntu and which belong to Alpha.
- Explain why arbitrary repository mixing is unsafe.
- Trace one Alpha capability from requirement to its Ubuntu primitive and Alpha integration layer.

## بعد از این فصل باید چه چیزی بلد باشم؟

باید بتوانی مرز Ubuntu و Alpha را توضیح بدهی، منبع مناسب برای یک قابلیت را انتخاب کنی و بدون ایجاد dependency یا security boundary نامشخص، یک integration طراحی کنی.

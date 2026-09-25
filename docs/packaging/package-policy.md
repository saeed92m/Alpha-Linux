# Alpha Linux Package Policy

## Principles

Alpha Linux distinguishes between:

1. Ubuntu-provided packages.
2. Upstream/open-source packages integrated by Alpha.
3. Alpha-maintained packages.
4. Third-party/vendor packages.
5. Proprietary software installed through legal user-controlled workflows.

## Requirements

Packages maintained by Alpha must define:

- package name and namespace;
- version;
- source;
- license;
- dependencies;
- build inputs;
- architecture support;
- maintainer information;
- changelog;
- reproducibility expectations;
- security status.

## Repository policy

Ubuntu repositories remain the foundation. Additional repositories must be explicitly evaluated, documented and controlled.

Blind mixing of Debian and Ubuntu repositories is prohibited.

## Signing

Release packages and repositories must use authenticated signing mechanisms before production distribution.

## Rollback

Package updates must participate in the Alpha update/recovery model where technically applicable.

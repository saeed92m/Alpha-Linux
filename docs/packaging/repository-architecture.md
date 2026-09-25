# Alpha Package Repository Architecture

## Repository layers

1. Ubuntu repositories — foundation.
2. Controlled upstream ecosystems — explicitly approved integrations.
3. Alpha repositories — Alpha-maintained packages.
4. Optional/vendor repositories — evaluated and documented.

## Separation

Repository origin must be visible in package metadata and release documentation.

Uncontrolled mixing of Debian and Ubuntu repositories is prohibited.

## Promotion

```
Source
→ Build
→ Test
→ Security Scan
→ Candidate
→ Validation
→ Signed Repository
→ Stable Promotion
```

## Architecturally required

- package metadata;
- architecture support;
- dependency policy;
- signing;
- repository metadata integrity;
- vulnerability tracking;
- rollback/update policy;
- retention policy.

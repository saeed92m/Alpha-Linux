# Alpha 0.1.0a1 Release Publication Contract

- The release manifest is immutable and binds release ID, Alpha version, actual artifact ID, artifact SHA-256, source commit, and CI run ID.
- Alpha prerelease versions use the project's `0.x` prerelease form.
- The deterministic tag is `v<version>`.
- Publication readiness requires every required gate to be explicitly passing; missing or failed gates block readiness.
- Planning has no tag creation, release publication, upload, network mutation, or repository mutation side effect.
- This contract covers the verified Python package artifact release only; it does not claim an OS ISO/IMG release.

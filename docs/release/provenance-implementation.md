# Artifact Provenance Implementation

Phase 1 implements the minimum provenance generator required for package artifacts.

The generator records source tree identity, artifact digest, build identity, timestamp, builder, toolchain, package/configuration identity, dependency inventory and test evidence.

The record is JSON and contains no credentials by design. Signature and promotion fields remain nullable until the release channel requires authenticated promotion.

This implementation is an evidence generator, not a release authorization mechanism. Release policy remains authoritative and CI gates remain the promotion authority.

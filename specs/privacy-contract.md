# Phase 6 Privacy Hardening Contract

## Purpose

This foundation defines immutable privacy classifications, purposes, retention and consent policies, requests, decisions, and bounded privacy plans.

## Semantics

Policy identifiers are normalized deterministically. A request is denied when no matching purpose exists, required consent is absent, or the request exceeds the policy retention window. These are planning semantics only.

## Boundary

No collection, storage, deletion, consent UI, identity access, network/filesystem mutation, subprocess execution, credential handling, or external privacy-service execution.

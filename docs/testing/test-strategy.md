# Alpha Linux Test Strategy

Testing is continuous and layered.

## Levels

1. Unit
2. Component
3. Integration
4. System
5. Installation
6. Upgrade
7. Rollback
8. Hardware compatibility
9. Security
10. Performance
11. Accessibility
12. Localization
13. Live ISO
14. Release candidate

## Evidence

Tests must produce machine-readable or otherwise reviewable evidence whenever practical.

## Regression

Every fixed release-critical defect should gain a regression test when technically feasible.

## Hardware

Hardware validation must record:

- Alpha release;
- kernel;
- relevant driver/firmware;
- hardware model;
- test result;
- limitations;
- reproduction notes.

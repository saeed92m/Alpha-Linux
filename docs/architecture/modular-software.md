# Alpha Linux Modular Software Architecture

**Status:** Active product direction under Change Request #290.

## Principle

Alpha Linux ships a minimal, complete workstation base. Applications are modular and independently selectable. The product must not require a user to install an entire domain bundle merely to obtain one application.

## Application vs bundle

**Application:** an independently installable package/application with its own dependency declaration.

**Bundle:** a convenience manifest containing multiple applications. A bundle is not required to install any member application.

Example: an Astronomy bundle may contain Stellarium, TOPCAT, DS9 and Astropy tooling. A user may install only one member or the whole bundle.

## Software Center behavior

The Software Center should expose individual applications, optional bundles, dependency summary, download size, estimated installed size, repository/source, licensing metadata where applicable, explicit install/remove action and update state. Before installation, the user should see what will actually be added.

## ISO policy

The ISO contains the Alpha Base + COSMIC + essential system integration. Large optional applications, datasets and specialist stacks remain online/installable unless there is a release-specific reason to ship them in the base.

## Profiles

Profiles are convenience selections, not mandatory dependency layers: AI & Automation; Development; Engineering & CAD; Science & Astronomy; Aerospace; Networking & Security; Media & Creative; Office.

Profiles may be applied after installation or on a persistent portable system.

## Portable implication

The same package/application model is used in Installed and Portable Persistent modes. An application installed on the portable system persists because the package database and relevant filesystem state live on the persistent Alpha media.

## Non-goals

This architecture does not require a new package manager. Ubuntu/Debian package mechanisms remain the foundation. Alpha adds catalog, grouping, safety, UX and provenance around them. It also does not require shipping domain datasets inside the OS image.

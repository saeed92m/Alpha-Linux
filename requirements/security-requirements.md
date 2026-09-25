# Alpha Linux — Security Requirements

| ID | Requirement | Validation |
|---|---|---|
| AL-SEC-0001 | Privileged operations shall use least privilege and explicit authorization. | Security test |
| AL-SEC-0002 | AI-generated plans shall never constitute authorization by themselves. | Security test |
| AL-SEC-0003 | Destructive or administrative AI actions shall require the applicable approval level unless a separately documented safe policy permits autonomous execution. | Security/UX test |
| AL-SEC-0004 | Secrets shall not be embedded in source code, images or ordinary logs. | Static/security test |
| AL-SEC-0005 | Production artifacts shall use authenticated integrity mechanisms appropriate to their distribution channel. | Release test |
| AL-SEC-0006 | Alpha shall maintain a software/dependency inventory sufficient for vulnerability and provenance management. | Supply-chain audit |
| AL-SEC-0007 | Plugin and agent capabilities shall be subject to trust, permission and isolation controls appropriate to their risk. | Security test |
| AL-SEC-0008 | Privacy-sensitive data collection shall be explicit, minimized and controllable by the user. | Privacy audit |
| AL-SEC-0009 | Recovery mechanisms shall preserve security boundaries and shall not silently bypass authentication or encryption protections. | Recovery/security test |
| AL-SEC-0010 | Security-critical changes shall receive documented review before stable release. | Release audit |

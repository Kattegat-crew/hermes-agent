---
name: canton-network-repos
description: "Use when developing Daml apps on Canton Network."
tags: [canton, daml, smart-contracts, blockchain, localnet, api, jwt]
license: MIT
compatibility: opencode
---

# Canton Network Best Practices

Development practices for Canton Network and Daml decentralized applications.

## Guidelines
1. **Daml Smart Contracts**: Write modular Daml templates with explicit signatories and observers.
2. **LocalNet Environment**: Use `make` commands and Nix environments to manage Canton LocalNet instances.
3. **API Integration**: Connect frontends using the Canton JSON API or gRPC client libraries with strict JWT validation.

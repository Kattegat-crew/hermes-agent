---
name: domain-driven-design
description: 'Domain-Driven Design (DDD) principles: Bounded Contexts, Aggregates,
  Value Objects, and Ubiquitous Language.'
license: MIT
compatibility: opencode
---


# Domain-Driven Design (DDD)

Guidelines for tackling complex domain logic using strategic and tactical DDD.

## Tactical Patterns
1. **Entities vs Value Objects**: Entities have unique IDs and lifecycles. Value Objects are immutable, defined only by their attributes.
2. **Aggregates & Aggregate Roots**: Enforce business invariants within transactional boundaries. Only the Aggregate Root is referenced externally.
3. **Domain Events**: Capture significant occurrences in the domain (`OrderPlaced`, `UserRegistered`) to enable asynchronous side effects.
4. **Repositories**: Return complete Aggregates and abstract away storage mechanisms.

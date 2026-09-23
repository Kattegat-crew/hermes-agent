---
name: ads-destination-compliance
description: "Audit ad rejections at the destination when copy is clean"
license: Apache-2.0
metadata:
  author: Ragnar
  version: "1.0"
---

# Ads Destination Compliance (venue-first)

Class skill for paid-social work in restricted verticals (online gambling,
physical casinos, supplements, credit). Core doctrine: platforms evaluate the
**ad + destination pair**, not the copy alone. A perfectly clean copy is
guaranteed rejection if the landing facilitates the restricted behavior.

## Activation contract

Use when paid ads get rejected repeatedly, when an ad account gets restricted
for policy/integrity, when planning landing pages that paid traffic will hit,
or when adapting organic content into ad-ready pieces.

## Triage sequence for repeated rejections

1. Pull the exact rejection reason per ad and count rejections over time —
   reiteration itself escalates enforcement.
2. If the reason is a restricted-vertical policy, STOP editing copy. Audit the
   **landing** for restricted affordances: playable games, bonus/credito
   canjeable, deposit or account-creation paths, prizes with amounts.
3. Fix the destination, not the text: point the ad at an ad-safe page
   (venue-first below). Changing copy while the destination violates the
   policy produces one more rejection.
4. Once restricted, accounts only accrue strikes: **do not create or duplicate
   ads** ('- Copia') while restricted — every attempt feeds the repetition
   case. Appeal the review and file the vertical-authorization docs in
   parallel; both tracks run without touching ads.
5. Watch twin risk: sibling brand accounts running the same destination
   pattern inherit the same rejection loop.

## Venue-first pattern (ad-safe landing)

For physical venues in a gambling-restricted market, the exception survives
only if the destination does not promote or facilitate online play. The
ad-safe shape: place + event + date as the hero, room ambience gallery,
brand host block, location/schedule for venues (closed venues excluded),
lead-capture form, legal footer (+18 / regulator, carried by ART not copy).
Game mechanics, prize amounts and accumulated totals are REMOVED from the
page (moved to T&C) until authorization is granted.

House standard (fixed by the Admin): organic copy IS ad copy — every piece
ships ad-ready in two uses (organic 30s / paid 15s) with compliance as a
design layer, not a post-hoc lint. Compliance lint is deterministic and runs
BEFORE any paid gate: banned vocabulary, prize amounts, mechanics.

## Colombia / Coljuegos notes (as of 2026-09)

Meta allows physical-casino and in-venue entertainment ads without prior
authorization; Colombia is not in the unsupported-markets list. The
exception is voided when the ad OR its landing promotes online play (digital
roulette/slots with redeemable bonus voided it for our client). Commercial
vocabulary rules: qualitative only (no prize amounts), no legal fine print in
copy (art carries it), no game mechanics, experience-first framing.

## Case pointers

- Restricted-account case: brain/ops/caso-cuenta-ads-golden-2026-09-19.md
- Repo docs (marketing-campaign-generator, commit 171c0bf): docs/ads/
  POLITICAS-META-GOOGLE-ADS-2026-09-18.md, ESTRUCTURA-VIDEO-ADS,
  docs/planes/PLAN-ADS-MASIVOS y PLAN-AD-READY (same date).

Never auto-correct and republish a rejected ad; register, fix destination,
and re-submit through the human.


---

## Procedencia

Absorbido por F3 el 20260923-055337 desde la autoskill `data/skills/ads-destination-compliance` (sin versión en git hasta hoy).
El procedimiento se conserva íntegro; el paraguas `meta-ads-ops` es su punto de entrada.


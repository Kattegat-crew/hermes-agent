---
name: campaign-content-intelligence
description: "Use when analyzing published campaign content per client."
version: 1.0.0
author: Ragnar
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [marketing, analytics, content, metrics, instagram, facebook, benchmark, optimization]
    related_skills: [composio-social-publishing, outline-wiki-ops]
---

# Campaign Content Intelligence

Turn published campaign content into a reusable **performance dataset** so each new campaign is briefed
with data, not intuition. Class-level: it covers reels, posts, carousels AND stories, and it is always
**per client** (benchmarks normalized per brand, never compared across brands).

## Golden rule — the analysis unit is the FINAL PUBLISHED REEL

Analyze the published artifact (finished reel with music/cartelas/palette), NOT the raw generated clips.
The raw clips drive production QA; the published reel drives performance. The platform media_id is the join key.

## The four axes measured

| Axis | Metric | Tool |
|---|---|---|
| Rhythm | words/sec, seconds of silence, phrase density | faster-whisper (`word_timestamps=True`) |
| Editing | cut count, mean/median shot duration, fps | ffprobe + scene detection (`select='gt(scene,0.3)'`) |
| Audio | LUFS, true peak, band energy, BPM | ffmpeg `ebur128` + scipy spectral |
| Script/CTA | exact second of each beat, when like/save/comment/follow is asked, repeated phrases | transcript aligned + CTA regex |

## Pipeline (5 layers)

1. **Registry (source of truth)** — every publication (reel/story/post/carousel) recorded with brand,
   campaign, format, platform, media_id, asset, url, timestamp. One store per client.
2. **Harvest (Composio)** — IG: `views, reach, likes, comments, saved, shares, total_interactions, reposts`,
   reels-only `ig_reels_avg_watch_time`/`reels_skip_rate`, stories `link_clicks`/`replies`/`follows`;
   FB: `post_media_view`. Stories MUST be harvested live (expire in 24h); reels/posts batch-harvested daily.
   Exact slugs, required fields and deprecation warnings live in the `composio-social-publishing` skill's
   `references/platform-metrics-schemas.md`.
3. **Feature extraction (local)** — on the final asset via ffprobe/ffmpeg/scipy/faster-whisper.
4. **Analysis** — normalize (views per follower, per day, per format), compute per-brand per-format benchmarks
   and correlation of features to performance.
5. **Feedback loop** — verdicts of the prior batch are injected into the NEXT campaign brief
   (e.g. "hooks <1s + CTA <3s gave +X% views") so Bragi/Sindri adjust with data.

## Per-client storage and rendering

- **Raw data**: store per client (tables/files `golden`, `lucky`) in a JSONL/SQLite operational store on the
  VPS. The wiki is NOT for volatile time-series — it becomes a pile of versions.
- **Human-readable analysis**: render a page per campaign into the client's **wiki collection**
  (1 collection = 1 company is already the approved model), path e.g. `Golden SAS -> Campañas -> Sept2026 -> Análisis`.
- Flow: `crudo -> análisis -> render -> página en carpeta wiki del cliente`.

## Owner agents (from the approved roster)

- **Freyja (Social)** — registers content at publish time (has the media_id).
- **Heimdall (Analytics)** — owns the whole pipeline: harvest, features, analysis, benchmarks, renders the
  wiki page. No other agent touches it.

## Design decisions already made with the Admin

- The repo that hosts this (and the whole campaign workflow) is being renamed
  `video-ai-generator` -> `marketing-campaign-generator`; it is the SAME repo, the hub of the entire
  automated campaign generation workflow. Rename detail in `references/repo-rename-playbook.md`.
- Raw store = JSONL/SQLite (VPS) for computing; wiki (per client) for showing. Both, each its own job.

## Pitfalls

- **Regression needs n >= 10 published reels** to say anything. With 1 reel there is no signal — build the
  dataset first, then interpret.
- **Do not borrow another audience's benchmarks.** Saul's viral-metrics ranges are from a different content
  type; calibrate YOUR ranges per brand (views/follower, per day).
- **IG insights** require Business/Creator account + >=1,000 followers + media within 2 years + FINISHED
  status. FB metrics `post_impressions`/`post_engagements` etc. deprecated Nov 15 2025 — only `post_media_view` survives.
- **Stories cannot be backfilled** — harvest them live or they are lost forever.

---
name: web-performance-core-vitals
description: Web performance optimization, Core Web Vitals (LCP, INP, CLS), bundle analysis, and rendering performance.
license: MIT
compatibility: opencode
---

# Web Performance & Core Web Vitals

Mastery guide for optimizing web application speed and responsiveness.

## Target Metrics
- **LCP (Largest Contentful Paint)**: < 2.5s
- **INP (Interaction to Next Paint)**: < 200ms
- **CLS (Cumulative Layout Shift)**: < 0.1

## Optimization Checklist
1. **Image Optimization**: Use WebP/AVIF, explicit `width`/`height` to avoid layout shifts, and responsive `srcset`.
2. **Font Loading**: Use `font-display: swap` and preload critical self-hosted fonts.
3. **Code Splitting**: Dynamic imports for heavy dialogs, rich text editors, and charting libraries.
4. **Server-Side Caching**: CDN edge caching, stale-while-revalidate headers, and asset compression (Brotli/Gzip).

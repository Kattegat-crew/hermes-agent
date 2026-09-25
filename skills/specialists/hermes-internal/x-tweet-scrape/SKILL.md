---
name: x-tweet-scrape
description: "Use when extracting tweet or X Article content by URL."
tags: [twitter, x, scraping, scrape, fixupx, fxtwitter, articulo, metadata]
---

# X/Twitter Tweet Scraping Skill

## Overview
Extract full tweet text, media, user info, and metrics from X/Twitter using multiple strategies.

## Method 1: fixupx.com Metadata Extraction (Primary — No Auth, No Playwright)
Convert `x.com/...` to `fixupx.com/...` and extract metadata from HTML with urllib:

```python
import urllib.request, re

tweet_url = "https://x.com/i/status/2084986801652174943"
url = tweet_url.replace("x.com", "fixupx.com").replace("twitter.com", "fixupx.com")
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode("utf-8")

# Extract OG tags and structured metadata
og_desc = re.search(r'<meta property="og:description" content="([^"]+)"', html)
title = re.search(r'<meta property="og:title" content="([^"]+)"', html)
image = re.search(r'<meta property="og:image" content="([^"]+)"', html)
pub_time = re.search(r'<meta property="article:published_time" content="([^"]+)"', html)
author_url = re.search(r'<meta property="article:author" content="([^"]+)"', html)

# Extract engagement metrics from structured data
# Primary: meta tags (may fail on some pages)
likes = re.search(r'<meta content=\"Likes\"[^>]+><meta content=\"(\\d+)\"', html)
retweets = re.search(r'<meta content=\"Retweets\"[^>]+><meta content=\"(\\d+)\"', html)
replies = re.search(r'<meta content=\"Replies\"[^>]+><meta content=\"(\\d+)\"', html)
views = re.search(r'<meta content=\"Views\"[^>]+><meta content=\"(\\d+)\"', html)

# Fallback: raw number patterns in fixupx HTML (more reliable)
# These use the actual JSON keys from the page source
likes_fb = re.search(r'favorite_count[^:]*:[\s]*(\d+)', html)
retweets_fb = re.search(r'retweet_count[^:]*:[\s]*(\d+)', html)
replies_fb = re.search(r'reply_count[^:]*:[\s]*(\d+)', html)

# Use fallback if primary failed
likes = likes or likes_fb
retweets = retweets or retweets_fb
replies = replies or replies_fb
```

## Method 2: FXTwitter API (Fallback — No Auth)
```python
import urllib.request, json

api_url = tweet_url.replace("x.com", "api.fxtwitter.com").replace("twitter.com", "api.fxtwitter.com")
req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as resp:
    data = json.loads(resp.read().decode("utf-8"))
    return data.get("tweet", {})
```

**⚠️ Warning:** FXTwitter may fail with DNS resolution errors (`No address associated with hostname`) on some VPS setups. In that case, fall back directly to fixupx.com metadata extraction.

## Method 3: Nitter Scraper (Fallback for text content)
Script at `/opt/data/scripts/tweet-scraper.py`:
```bash
python3 /opt/data/scripts/tweet-scraper.py "https://x.com/..." 
```
Returns format: `AUTOR: [name]\nTEXTO: [content]`

## X Article Handling (Critical — Tweet is link-only)

**Detect:** Tweet text is empty or only contains a t.co link.
**Resolve the t.co link** to find the target:

```python
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None
opener = urllib.request.build_opener(NoRedirect)
req = urllib.request.Request("https://t.co/ScYKUMp4Ll", headers={"User-Agent": "Mozilla/5.0"})
try:
    with opener.open(req, timeout=15) as r:
        destination = r.headers.get("Location")
except urllib.error.HTTPError as e:
    destination = e.headers.get("Location")
```

**If destination is `x.com/i/article/{id}`:**
1. **Método preferido (verificado 28/08):** `api.fxtwitter.com/<user>/status/<tweet_id>` devuelve `tweet.article` COMPLETO (title, preview_text, content.blocks[] en formato Draft.js) sin login. Recupera ~5K chars de artículos largos.
```python
import urllib.request, json
# tweet original (puede ser el id del status, no el id del article)
api_url = f"https://api.fxtwitter.com/{author}/{tweet_id}"
data = json.loads(urllib.request.urlopen(urllib.request.Request(api_url, headers={"User-Agent":"Mozilla/5.0"}), timeout=15).read())
art = data["tweet"]["article"]
# render de blocks: header-two→##, list items→-, code-block→fenced
print(art["title"], art["content"])
```
   (El id del tweet viene de la URL del status original; a veces el `/i/article/{id}` hay que resolverlo al post que lo contiene.)
2. **Fallback:** Los otros métodos (fixupx metadata + búsqueda externa en DuckDuckGo) siguen valiendo si FXTwitter no trae el article.
3. **SSL cert issues:** Algunos sitios usan certs self-signed. Usar contexto no verificado:
```python
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE
urllib.request.urlopen(req, timeout=20, context=ssl_ctx)
```

## Extraction Chain Priority
1. fixupx.com metadata extraction → OG description, author, engagement, image
2. If tweet is link-only → resolve t.co → detect if X Article
3. If X Article → search for title on DuckDuckGo → find full content on external newsletter/site
4. If no external source found → save what we have (metadata only)

## Video Tweet Detection
- **When t.co link resolves to `twitter.com/.../video/1`** → the tweet is a native video tweet, not an external link
- The `amplify_video_thumb` image in the HTML is the video thumbnail
- No need to search for external content in this case — the tweet content IS the video
- Example: `https://x.com/i/status/2085019745221554678` → t.co resolved to `twitter.com/imbabybrooklyn/status/2085019745221554678/video/1`

## Notes
- fixupx.com works without authentication and returns rich metadata including engagement stats
- X Articles (`/i/article/`) require a logged-in browser — cannot extract body via urllib
- Newsletter platforms (ConvertKit, beehiiv, Substack) often republish X Article content externally
- Use `re.search` on fixupx.com HTML for all metadata extraction — it's fast and reliable
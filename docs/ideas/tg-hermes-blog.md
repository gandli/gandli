# tg-hermes-blog

> Auto-publish tagged conversations between me and my Telegram Hermes-Agent bot as a public micro-blog, hosted on Cloudflare.

**Status:** 🆕 Designed · **Stack:** Cloudflare Workers + D1 + Astro SSR + Python cron · **Inspired by:** [miantiao-me/BroadcastChannel](https://github.com/miantiao-me/BroadcastChannel)

## The itch

I already talk to my Telegram Hermes bot every day — that's where my thinking gets rehearsed. I want the messages tagged `#blog` to become a public feed, without me copy-pasting anything, and without giving anyone else my Hermes SQLite.

## Non-goals

- ❌ Not a full CMS — no editor, no admin UI
- ❌ Not real-time — 5-min lag is fine
- ❌ Not a Telegram bot rewrite — Hermes stays untouched

## Architecture

```mermaid
flowchart LR
    subgraph LOCAL["🖥️ Mac mini (local)"]
        HERMES[(Hermes SQLite<br/>~/.hermes/sessions.db)]
        CRON[cron sync.py<br/>every 5 min]
    end

    subgraph CF["☁️ Cloudflare"]
        INGEST[Worker /ingest<br/>Bearer auth]
        D1[(D1 Database<br/>sessions/posts/tags)]
        BLOG[Astro SSR Worker<br/>*.workers.dev]
    end

    READER([Public reader])

    HERMES -->|SELECT WHERE id > watermark<br/>AND content LIKE '%#blog%'| CRON
    CRON -->|POST JSON + Bearer| INGEST
    INGEST --> D1
    BLOG -->|read| D1
    READER --> BLOG

classDef localStyle fill:#e3f2fd,stroke:#2196f3,stroke-width:2px,color:#000
classDef cfStyle fill:#fff3e0,stroke:#ff9800,stroke-width:2px,color:#000
classDef dataStyle fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px,color:#000
classDef userStyle fill:#e8f5e8,stroke:#4caf50,stroke-width:3px,color:#000

class HERMES,CRON localStyle
class INGEST,BLOG cfStyle
class D1 dataStyle
class READER userStyle
```

## Data model (D1)

```sql
CREATE TABLE sessions (
  session_id TEXT PRIMARY KEY,
  title      TEXT,
  created_at INTEGER,
  updated_at INTEGER
);

CREATE TABLE posts (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT REFERENCES sessions(session_id),
  message_id INTEGER,           -- Hermes message.id
  role       TEXT,              -- 'user' | 'assistant'
  content    TEXT,
  ts         INTEGER,
  published  BOOLEAN DEFAULT 0,
  raw_json   TEXT,
  UNIQUE(session_id, message_id)
);

CREATE TABLE tags (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id INTEGER REFERENCES posts(id),
  tag     TEXT
);

CREATE TABLE media (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id INTEGER REFERENCES posts(id),
  type    TEXT,   -- 'image' | 'file' | 'link'
  url     TEXT,
  alt     TEXT
);

CREATE TABLE watermarks (
  key   TEXT PRIMARY KEY,       -- 'last_synced_id'
  value INTEGER
);
```

## Sync sequence

```mermaid
sequenceDiagram
    autonumber
    participant Cron as cron sync.py
    participant DB as Hermes SQLite
    participant W as CF Worker /ingest
    participant D1 as D1

    Cron->>D1: GET /watermark
    D1-->>Cron: last_synced_id = 12934
    Cron->>DB: SELECT * FROM messages<br/>WHERE id > 12934 AND content LIKE '%#blog%'
    DB-->>Cron: rows[42]
    Cron->>Cron: normalize + extract tags/media
    Cron->>W: POST /ingest {rows} + Bearer
    W->>W: verify token
    W->>D1: UPSERT posts/tags/media
    W->>D1: UPDATE watermark = max(id)
    W-->>Cron: 200 OK {inserted: 42}
```

## Message state machine

```mermaid
stateDiagram-v2
    [*] --> Hermes: user/assistant message
    Hermes --> Pending: content matches #blog
    Hermes --> Ignored: no #blog tag
    Pending --> Synced: cron pulls it
    Synced --> Published: worker writes D1
    Published --> Retracted: contains #unblog<br/>(future)
    Retracted --> [*]
    Ignored --> [*]
```

## Trigger rules

- **Publish**: any message containing `#blog` (case-insensitive)
- **Idempotent**: `(session_id, message_id)` unique — safe re-runs
- **Retract** (later): `#unblog` sets `published = 0`
- **Series**: `#blog:series-name` groups into a series page

## Open questions

- [ ] Feed-level RSS? (probably yes — reuse Astro's RSS integration)
- [ ] Full-text search? (D1 has FTS5 via virtual table — cheap)
- [ ] Comments? (out of scope — link to Telegram if reader wants to reply)
- [ ] Domain? (start on `*.workers.dev`, custom domain later)

## Why not…

| Alternative | Why not |
|---|---|
| Telegram Bot API webhook | Bot can't read its own replies verbatim |
| Fork BroadcastChannel as-is | Data source is `t.me/s/xxx` public channels — I don't want a public Telegram channel |
| Notion + public page | Requires me to move messages out of Telegram |
| Cross-post via Telegram → Zapier → CMS | Fragile, chain of proprietary hops |

## Milestones

1. ✅ Design docs (this file + diagrams)
2. Probe Hermes SQLite schema, write `sync/sync.py`
3. Cloudflare account + D1 database + `wrangler.toml`
4. Worker `/ingest` with Bearer auth
5. Fork BroadcastChannel, swap `src/lib/data.ts` to read from D1
6. Deploy to `*.workers.dev`, post first `#blog` message

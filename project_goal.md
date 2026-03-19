# Project Goal: Revive Knightfall — A Daring Journey

## Mission
Grow Knightfall: A Daring Journey's daily active player count from ~21 to **100+ players/day** within 8 weeks, using only free, low-effort, largely automated methods.

## The Game
- **Title:** Knightfall: A Daring Journey
- **Developer:** Landfall Games
- **Platform:** Steam (PC only, free to play)
- **Genre:** Horse-drifting Battle Royale (28-player matches, teams of 2)
- **Status:** ~21 daily players as of March 2026, peak was 1,512 (June 2024)
- **Steam App ID:** 1911390
- **Review score:** 90% positive (~8,000 reviews) — people like it, they just don't know it exists or can't find matches

## Why It's Solvable
The game isn't bad — it died from a **matchmaking death spiral**, not from poor quality. With enough players concentrated into the same time window, matches fill and the experience works. The barrier to entry is zero (free game). The content potential is high (funny, absurd, visual).

## Success Metric
**Primary:** 100+ daily active players sustained for 2+ consecutive weeks
**Proxy (trackable weekly):** Steam concurrent peak ≥ 15 players during scheduled play window

## Hard Constraints
- Budget: $0
- Time: < 1 hour/week of manual effort
- Platforms available: Steam, Discord, TikTok, YouTube
- Recording: Available and set up
- Everything possible must be automated or templated

## Approach Overview
Three phases, each building on the last:

| Phase | Goal | Timeframe | Effort |
|-------|------|-----------|--------|
| 1 — Concentrate | Sync existing players into daily time window | Week 1–2 | One-time setup (~30 min) |
| 2 — Amplify | Drive new installs via clips + creator outreach | Week 2–6 | ~30 min/week |
| 3 — Retain | Keep players engaged with recurring events | Week 4+ | ~15 min/week (automated reminders) |

## Workflows (Execution SOPs)
Each workflow is a step-by-step SOP with time estimates and tool references.

| # | Workflow | Frequency | Time cost |
|---|----------|-----------|-----------|
| 01 | [Track Player Count](workflows/01_track_player_count.md) | Automated daily | 0 min/week |
| 02 | [Post Steam Revival Thread](workflows/02_post_steam_revival_thread.md) | One-time | 15 min total |
| 03 | [Post TikTok Clip](workflows/03_tiktok_clip_pipeline.md) | Weekly | ~20 min/clip |
| 04 | [Creator Outreach](workflows/04_creator_outreach.md) | One-time + follow-up | ~20 min total |
| 05 | [Discord Setup & Scheduling](workflows/05_discord_setup.md) | One-time setup | ~30 min total |

## Existing Community Assets (Don't Rebuild These)
- **Rosefall Discord** — largest Knightfall community, already runs events
- **knightfallbr.com Discord** — official-ish, runs biweekly events with custom mods
- Both already have organized play sessions — our job is to amplify them, not compete

## Weekly Routine (< 1 hour total)
1. Run `tools/track_player_count.py` — check if numbers are trending (automated, 0 min)
2. Post one TikTok clip from last session — 20 min max
3. If creators contacted: check for replies — 5 min

That's it. Everything else is one-time setup.

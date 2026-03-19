# Knightfall Revival

**Mission:** Grow Knightfall: A Daring Journey from ~11 daily players to **100+** in 8 weeks.
**Constraints:** $0 budget · <1 hr/week manual effort · Steam, Discord, TikTok, YouTube only.

---

## The Game

| | |
|---|---|
| Title | Knightfall: A Daring Journey |
| Developer | Landfall Games |
| Platform | Steam — free to play |
| Genre | Horse-drifting Battle Royale (28-player, teams of 2) |
| Steam App ID | 1911390 |
| Reviews | 90% positive (~8,000 reviews) |
| Peak players | 1,512 (June 2024) |
| Status | ~11 daily players as of March 2026 |

**Why it's solvable:** The game didn't die from bad quality — it hit a matchmaking death spiral. Enough players concentrated into the same time window = matches fill = the game works again. Barrier to entry: zero (free).

---

## 3-Phase Strategy

| Phase | Goal | Timeframe | Effort |
|-------|------|-----------|--------|
| 1 — Concentrate | Sync existing players into one daily time window | Week 1–2 | ~30 min one-time |
| 2 — Amplify | Drive new installs via clips + creator outreach | Week 2–6 | ~30 min/week |
| 3 — Retain | Keep players coming back with recurring events | Week 4+ | ~15 min/week |

---

## One-Time Setup (do these in order)

**Step 1 — Configure email alerts** (10 min)
1. Create a Gmail App Password: Google Account → Security → 2-Step Verification → App passwords
2. Add secrets at `github.com/gregorioguirado/Knighfall-Revival/settings/secrets/actions`:
   - `GMAIL_USER` → your Gmail address
   - `GMAIL_APP_PASSWORD` → the app password from step 1
3. Edit `config/subscribers.csv` to add alert recipients
4. Edit `config/settings.json` to set your alert thresholds

**Step 2 — Join the Discord** (30 min)
- Follow [workflows/05_discord_setup.md](workflows/05_discord_setup.md)
- Main community: **discord.gg/Jt58UeZf**
- Goal: find out the agreed daily play time window

**Step 3 — Post the Steam revival thread** (15 min)
- Follow [workflows/02_post_steam_revival_thread.md](workflows/02_post_steam_revival_thread.md)
- Template is ready — fill in Discord link + play time from Step 2

**Step 4 — Run Instagram creator outreach** (20 min)
- Follow [workflows/04_creator_outreach.md](workflows/04_creator_outreach.md)
- You already have target accounts — use the DM template, log results

**Step 5 — Post your first clip** (20 min)
- Follow [workflows/03_tiktok_clip_pipeline.md](workflows/03_tiktok_clip_pipeline.md)
- One clip to TikTok and/or YouTube Shorts — start the habit now

---

## Weekly Routine (< 30 min total)

| Task | Time | How |
|------|------|-----|
| Check player count trend | 0 min | Automated — check email or `data/player_count_log.csv` |
| Post one TikTok / Shorts clip | 20 min | [workflows/03_tiktok_clip_pipeline.md](workflows/03_tiktok_clip_pipeline.md) |
| Check Instagram DM replies | 5 min | Instagram app |

---

## File Structure

```
.env                          ← secrets (gitignored — copy from .env.example)
config/
  settings.json               ← alert thresholds + game config (edit this)
  subscribers.csv             ← who gets email alerts (edit this)
data/
  player_count_log.csv        ← auto-updated daily by GitHub Actions
tools/
  track_player_count.py       ← run manually or via GitHub Actions
  trigger_workflow.py         ← trigger GitHub Actions from terminal
workflows/
  01_track_player_count.md
  02_post_steam_revival_thread.md
  03_tiktok_clip_pipeline.md
  04_creator_outreach.md
  05_discord_setup.md
.github/workflows/
  track_players.yml           ← runs daily at 8pm UTC, commits log, sends alerts
```

---

## When to ask Claude for help
- Something in a workflow is unclear or blocked
- Player count spikes and you want to capitalise fast
- You want to contact Landfall and need a message drafted
- You want to add new channels or automate more

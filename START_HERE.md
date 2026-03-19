# Start Here

You want to revive Knightfall: A Daring Journey to 100 daily players.
Everything is defined. Follow the steps in order.

---

## Step 0 — Push this repo to GitHub (5 min, one-time)
The repo already exists at: **https://github.com/gregorioguirado/Knighfall-Revival**

Run these commands in this project folder:
```
git init
git add .
git commit -m "init: WAT framework setup for Knightfall revival"
git branch -M main
git remote add origin https://github.com/gregorioguirado/Knighfall-Revival.git
git push -u origin main
```

---

## Step 1 — Set up the automated tracker (10 min, one-time)
Follow [Workflow 01](workflows/01_track_player_count.md) — full instructions there.

Short version:
1. Create a Gmail App Password (Google Account → Security → App passwords)
2. Add 4 secrets to: https://github.com/gregorioguirado/Knighfall-Revival/settings/secrets/actions
3. Trigger the Action manually once to verify it works

After this: player count is logged daily at 8pm UTC, you get emailed at milestones (30/50/100). No PC needed. View logs at:
https://github.com/gregorioguirado/Knighfall-Revival/blob/main/data/player_count_log.csv

---

## Step 2 — Join the Discord (30 min, one-time)
Follow [Workflow 05](workflows/05_discord_setup.md).

Main community: **https://discord.gg/Jt58UeZf**

Get the agreed daily play time. Save it — you'll need it for Step 3.

---

## Step 3 — Post the Steam thread (15 min, one-time)
Follow [Workflow 02](workflows/02_post_steam_revival_thread.md).
Template is ready. Fill in the Discord link and play time from Step 2. Copy, paste, post.

---

## Step 4 — Start posting clips (20 min/week, ongoing)
Follow [Workflow 03](workflows/03_tiktok_clip_pipeline.md).
One clip per week to TikTok and/or YouTube Shorts. This is the highest-reach action you have.

---

## Step 5 — Run Instagram creator outreach (20 min, one-time)
Follow [Workflow 04](workflows/04_creator_outreach.md).
You have target accounts already. Use the DM template. Log in `.tmp/creator_targets.csv`.

---

## Weekly Routine After Setup (< 30 min total)
| Task | Time | How |
|------|------|-----|
| Check player count log | 1 min | https://github.com/gregorioguirado/Knighfall-Revival/blob/main/data/player_count_log.csv |
| Post one TikTok/Shorts clip | 20 min | [Workflow 03](workflows/03_tiktok_clip_pipeline.md) |
| Check Instagram DM replies | 5 min | Instagram app |

That's the whole job. Steps 0–5 are one-time. The table above is recurring.

---

## When to ask Claude for help
- Something in a workflow is unclear or blocked
- Player count spikes and you want to capitalize fast
- You want to contact Landfall and need a message drafted
- You want to add new channels or automate more

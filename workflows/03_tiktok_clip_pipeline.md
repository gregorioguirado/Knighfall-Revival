# Workflow 03: Post TikTok / YouTube Shorts Clip

## Objective
Post one short clip per week of Knightfall gameplay to TikTok and/or YouTube Shorts. The game is visually absurd and funny — clips are the lowest-effort, highest-reach way to drive new installs since the game is free.

## Frequency
Weekly. 1 clip minimum, 2–3 if moments are good.

## Time Cost
**~20 minutes per clip** (find moment → trim → caption → post)

## Why This Works
- The game is free → zero friction from viewer to player
- Horse-drifting + shotguns = inherently shareable content
- "Hidden gem" / "dying game" framing performs well on short-form
- One viral clip can outperform weeks of other effort

## Required Inputs
- Recording software already set up (OBS, ShadowPlay, etc.)
- TikTok account and/or YouTube account
- A clip worth posting (see Clip Criteria below)

## Clip Criteria — What to Look For
Good clips are usually one of these:
1. **Funny crash or chaos** — horse physics being absurd
2. **Clutch play** — last-second win, unexpected kill
3. **Big moment** — winning the match, reaching the castle
4. **Weird game situations** — things new players wouldn't expect

If nothing notable happened this session, don't force it. Wait for the next session.

## Steps

### During Play (0 extra minutes)
- Keep recording running the whole session (your setup is already ready)
- After session ends, roughly remember if anything clip-worthy happened

### Finding and Trimming the Clip (~10 min)
1. Open your recording in your editor (DaVinci Resolve free, CapCut, or even the Xbox Game Bar clip tool)
2. Cut it to **15–45 seconds** — no longer
3. Trim tight: start just before the action, end right after the payoff
4. No need for music, overlays, or editing — raw gameplay with game audio is fine

### Captioning (~5 min)
Use one of these caption formats (copy, adapt, post):

```
This free game has 20 players left and it's a crime
#knightfall #hiddengem #pcgaming #battleroyale #indiegame
```
```
Horse battle royale goes wrong (in the best way)
#knightfall #indiegame #pcgaming #funny
```
```
This game is dying and I refuse to let it
#knightfall #deadgame #hiddengem #indiegame
```

Always include: `#knightfall #indiegame #pcgaming`

### Posting (~5 min)
1. **TikTok**: Upload video → paste caption → post (no scheduled posting needed)
2. **YouTube Shorts**: Upload → title = same as caption → add to "Knightfall" playlist if you have one

Post to both if you have both accounts. Same clip, same caption.

## After Posting
- Save the post URL in `.tmp/links.txt` with the date
- Check back in 24 hours — if a comment asks "what game is this?", reply with the Steam link and Discord invite

## Tracking
Run `tools/track_player_count.py` the day after posting a clip. If the count spikes, the clip worked. Note it in `.tmp/player_count_log.csv` (the script does this automatically).

## Edge Cases
- **No good moments this week**: Skip. Don't post filler. Quality over quantity.
- **Clip gets traction (10k+ views)**: Pin a comment with the Steam link + Discord invite immediately
- **Comments are negative** ("this game is dead"): Respond once with "it's alive if you show up at [play time]" — don't argue

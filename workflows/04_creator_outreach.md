# Workflow 04: Creator Outreach (Instagram)

## Objective
Send a short DM to Instagram content creators who cover indie/niche PC games, inviting them to cover Knightfall. You already have a list of target accounts. One yes from a creator with an engaged audience can drive hundreds of installs in a day.

## Frequency
**One-time send (~20 min). Weekly reply check (~5 min).**

## Time Cost
- Initial outreach: ~20 minutes
- Reply monitoring: ~5 min/week

## Required Inputs
- Instagram account (logged in)
- Your list of target creator accounts
- Discord invite: https://discord.gg/Jt58UeZf

## Target Creator Profile
Prioritize accounts that match as many of these as possible:
- Posts PC gaming content (not console-only)
- Has covered "hidden gem", "underrated", "free game", or "dying game" content
- 10k–500k followers (bigger = less likely to respond; smaller = less reach)
- Posts at least monthly (still active)
- Landfall-adjacent: TABS, Rounds, Stick Fight fans are the warmest audience

## DM Template (Instagram)

Keep it short — long messages get ignored. Copy this exactly, fill in `[brackets]`:

```
Hey [Name]! I think your audience would love this weird free PC game —
Knightfall is a horse-drifting battle royale with 90% positive Steam reviews
but it's dying because not enough people know about it.

It's completely free. I can set up a full lobby so you'd actually get a real game
(not an empty server).

Steam: store.steampowered.com/app/1911390
Discord: discord.gg/Jt58UeZf

No pressure — just thought it fits your vibe!
```

**Do not add more.** Shorter = higher open and reply rate.

## Steps

1. Open `.tmp/creator_targets.csv` (create it if it doesn't exist — template below)
2. Go through your target account list, pick the top 5–10 that fit the profile above
3. Log each one in the CSV before DMing (so you don't double-send)
4. Send the DM on Instagram
5. Mark "contacted" = Yes and add the date in the CSV

### creator_targets.csv template
```
instagram_handle,followers_approx,contacted,contact_date,reply,notes
@handle1,50000,No,,,
@handle2,120000,No,,,
```

## Weekly Reply Check (5 min)
- Open Instagram DMs
- If someone replied: coordinate a play session via the Discord
- Log outcome in the CSV (reply = "Yes - interested" / "No" / "No response")
- After 2 weeks with no reply: move on, don't follow up again

## When a Creator Says Yes
1. Post in the Knightfall Discord (https://discord.gg/Jt58UeZf) asking players to show up at a specific time
2. Play — let them record freely
3. After they post: check `data/player_count_log.csv` for a spike the next day
4. Comment on their post with the Steam link + Discord invite if they haven't included it

## Tracking
After a creator posts content, run the player count tracker manually to capture the spike:
```
python tools/track_player_count.py
```

## Edge Cases
- **No response after 2 weeks**: Move on. Don't follow up.
- **Creator asks for payment**: Decline politely — budget is $0 and organic coverage is more credible.
- **Creator posts negative content**: Don't engage. Any coverage drives free installs.
- **Creator has < 10k followers**: Only pursue if their content is extremely niche-aligned (e.g. they already post about Landfall games).

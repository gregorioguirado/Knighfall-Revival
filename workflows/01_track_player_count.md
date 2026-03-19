# Workflow 01: Track Player Count

## Objective
Automatically log Knightfall's daily Steam player count via GitHub Actions — no PC required. View history anytime on GitHub. Get an email alert when milestones are crossed (30, 50, 100 players).

## Frequency
Daily at 8pm UTC (automated). You don't touch it.

## Time Cost
**~10 minutes one-time setup. 0 min/week after that.**

## How It Works
1. GitHub Actions runs `tools/track_player_count.py` every day at 8pm UTC
2. The script fetches the current Steam player count
3. The count is appended to `data/player_count_log.csv` and committed back to the repo
4. If the count crosses a milestone (30 / 50 / 100), a Gmail alert is sent to you
5. You can see the full log anytime at: https://github.com/gregorioguirado/Knighfall-Revival/blob/main/data/player_count_log.csv

---

## One-Time Setup

### Step 1 — Create a Gmail App Password (~3 min)
This lets GitHub send emails on your behalf without exposing your real password.

1. Go to your Google Account → Security → 2-Step Verification (must be enabled)
2. At the bottom of that page, click **App passwords**
3. Select app: **Mail** → Select device: **Other** → type "Knightfall Tracker" → **Generate**
4. Copy the 16-character password shown — you'll need it in Step 2

> If you don't see "App passwords", make sure 2-Step Verification is turned on first.

### Step 2 — Add Secrets to GitHub (~3 min)
Go to: **https://github.com/gregorioguirado/Knighfall-Revival/settings/secrets/actions**

Click **"New repository secret"** and add these four secrets one by one:

| Secret name | Value |
|-------------|-------|
| `GMAIL_USER` | Your Gmail address (e.g. `you@gmail.com`) |
| `GMAIL_APP_PASSWORD` | The 16-char App Password from Step 1 |
| `ALERT_EMAIL` | Where to send alerts (can be same as above) |
| `ALERT_THRESHOLD` | `30` (alert when count first exceeds 30) |

### Step 3 — Test it manually (~1 min)
Go to: **https://github.com/gregorioguirado/Knighfall-Revival/actions**
- Click **"Track Knightfall Player Count"**
- Click **"Run workflow"** → **"Run workflow"**
- Watch it run — should take ~20 seconds
- Check your email for an alert (if count > 30) and check the log file was updated

---

## Viewing the Data
No need to open anything locally. Just visit:
- **Log file**: https://github.com/gregorioguirado/Knighfall-Revival/blob/main/data/player_count_log.csv
- **Action runs**: https://github.com/gregorioguirado/Knighfall-Revival/actions

## Alert Triggers
Alerts fire once per milestone — you won't get spammed:
- **30 players** — Phase 1 is working, matches should be filling
- **50 players** — Phase 2 gaining traction
- **100 players** — Goal achieved

## Edge Cases
- **Action fails**: GitHub will email you automatically (GitHub's built-in failure notification). Check the Actions tab to see the error log.
- **Wants to change alert threshold**: Update the `ALERT_THRESHOLD` secret in GitHub settings.
- **Want to run it more often**: Edit the cron in `.github/workflows/track_players.yml`. E.g., `0 */6 * * *` = every 6 hours.

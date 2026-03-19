"""
Tool: track_player_count.py
Purpose: Fetch and log Knightfall's Steam concurrent player count.
         Sends a Gmail alert when count exceeds ALERT_THRESHOLD.
         Designed to run in GitHub Actions (daily cron) or locally.

Usage:
  python tools/track_player_count.py           # log current count + alert if needed
  python tools/track_player_count.py --summary # show trend report

Environment variables (set as GitHub Secrets or in .env):
  GMAIL_USER          sender Gmail address
  GMAIL_APP_PASSWORD  Gmail App Password (not your account password)
  ALERT_EMAIL         recipient address (can be same as GMAIL_USER)
  ALERT_THRESHOLD     integer, default 30 — alert when count exceeds this
"""

import requests
import csv
import os
import sys
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta, timezone

# Load .env if running locally
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

APP_ID = 1911390
PEAK_EVER = 1512  # Historical peak, June 2024
GOAL = 100

# Log file lives in data/ so it gets committed to the repo and is visible on GitHub
LOG_FILE = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "data", "player_count_log.csv")
)

GMAIL_USER = os.getenv("GMAIL_USER", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")
ALERT_EMAIL = os.getenv("ALERT_EMAIL", GMAIL_USER)
ALERT_THRESHOLD = int(os.getenv("ALERT_THRESHOLD", "30"))

# Milestone thresholds — alert fires once per milestone (tracked in log)
MILESTONES = [30, 50, 100]


# ---------------------------------------------------------------------------
# Steam API
# ---------------------------------------------------------------------------

def fetch_player_count():
    url = (
        "https://api.steampowered.com/ISteamUserStats/"
        f"GetNumberOfCurrentPlayers/v1/?appid={APP_ID}"
    )
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()["response"]["player_count"]
    except Exception as e:
        print(f"ERROR fetching player count: {e}")
        return None


# ---------------------------------------------------------------------------
# CSV log
# ---------------------------------------------------------------------------

def load_log():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, newline="") as f:
        return list(csv.DictReader(f))


def append_log(count, note=""):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    file_exists = os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "player_count", "note"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "player_count": str(count),
            "note": note,
        })


def highest_milestone_reached(rows):
    """Return the highest milestone already logged so we don't re-alert."""
    milestone_notes = [r["note"] for r in rows if r["note"].startswith("MILESTONE")]
    if not milestone_notes:
        return 0
    reached = [int(n.split(":")[1].strip()) for n in milestone_notes if ":" in n]
    return max(reached) if reached else 0


# ---------------------------------------------------------------------------
# Gmail alert
# ---------------------------------------------------------------------------

def send_gmail_alert(count, milestone=None):
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("ALERT: No Gmail credentials set — skipping email.")
        return

    subject = f"Knightfall alert: {count} players online!"
    if milestone == GOAL:
        subject = f"GOAL REACHED — Knightfall hit {count} players!"

    body = f"""Knightfall: A Daring Journey player count update

Current players online: {count}
Goal: {GOAL}
Progress: {min(100, round(count / GOAL * 100))}%
All-time peak: {PEAK_EVER}

View full log:
https://github.com/gregorioguirado/Knighfall-Revival/blob/main/data/player_count_log.csv

Keep going — post a clip or check the Discord.
https://discord.gg/Jt58UeZf
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = ALERT_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        print(f"Alert email sent to {ALERT_EMAIL}")
    except Exception as e:
        print(f"ERROR sending alert email: {e}")


# ---------------------------------------------------------------------------
# Summary report
# ---------------------------------------------------------------------------

def print_summary():
    rows = load_log()
    if not rows:
        print("No data yet. Run without --summary first.")
        return

    counts = [int(r["player_count"]) for r in rows if r["player_count"].isdigit()]
    if not counts:
        print("No valid count data found.")
        return

    latest = counts[-1]
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    recent = []
    for r in rows:
        try:
            ts = datetime.strptime(r["timestamp"], "%Y-%m-%d %H:%M UTC").replace(
                tzinfo=timezone.utc
            )
            if ts >= cutoff and r["player_count"].isdigit():
                recent.append(int(r["player_count"]))
        except ValueError:
            pass

    print("=" * 42)
    print("  KNIGHTFALL PLAYER COUNT SUMMARY")
    print("=" * 42)
    print(f"  Latest logged:    {latest}")
    if recent:
        print(f"  7-day average:    {sum(recent) / len(recent):.1f}")
    print(f"  All-time peak:    {PEAK_EVER}")
    print(f"  Goal:             {GOAL}")
    print(f"  Progress:         {min(100, round(latest / GOAL * 100))}%")
    print("=" * 42)

    if len(recent) >= 3:
        trend = recent[-1] - recent[0]
        if trend > 5:
            print("  TREND: UP — actions are working")
        elif trend < -5:
            print("  TREND: DOWN — try a different channel")
        else:
            print("  TREND: FLAT — needs a push (post a clip)")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if "--summary" in sys.argv:
        print_summary()
        return

    count = fetch_player_count()
    if count is None:
        append_log("ERROR")
        sys.exit(1)

    rows = load_log()
    prev_milestone = highest_milestone_reached(rows)

    # Determine if a new milestone was just crossed
    new_milestone = None
    for m in sorted(MILESTONES):
        if count >= m and m > prev_milestone:
            new_milestone = m

    note = f"MILESTONE: {new_milestone}" if new_milestone else ""
    append_log(count, note)

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"[{ts}] Knightfall players online: {count}")

    if count >= GOAL:
        print("GOAL REACHED — 100+ players!")
    elif count >= 30:
        print("Good — matches should be filling. Keep the momentum.")
    elif count >= 15:
        print("Getting there — keep posting clips.")
    else:
        print("Still low — focus on Discord coordination (Phase 1).")

    # Send alert on milestone or if count just crossed threshold
    if new_milestone:
        print(f"New milestone reached: {new_milestone} players!")
        send_gmail_alert(count, milestone=new_milestone)
    elif count >= ALERT_THRESHOLD and prev_milestone == 0:
        send_gmail_alert(count)


if __name__ == "__main__":
    main()

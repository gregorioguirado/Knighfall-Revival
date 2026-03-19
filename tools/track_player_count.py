"""
Tool: track_player_count.py
Purpose: Fetch and log Knightfall's Steam concurrent player count.
         Sends Gmail alerts to everyone in config/subscribers.csv at milestones.
         Designed to run in GitHub Actions (daily cron) or locally.

Usage:
  python tools/track_player_count.py           # log current count + alert if needed
  python tools/track_player_count.py --summary # show trend report

GitHub Secrets required (credentials only):
  GMAIL_USER          sender Gmail address
  GMAIL_APP_PASSWORD  Gmail App Password (not your account password)

All other config lives in config/settings.json and config/subscribers.csv.
"""

import requests
import csv
import json
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta, timezone

# Load .env if running locally
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
LOG_FILE        = os.path.join(ROOT, "data",   "player_count_log.csv")
SETTINGS_FILE   = os.path.join(ROOT, "config", "settings.json")
SUBSCRIBERS_FILE = os.path.join(ROOT, "config", "subscribers.csv")
TEMPLATE_FILE   = os.path.join(ROOT, "html",  "email_alert_template.html")

LOG_URL     = "https://github.com/gregorioguirado/Knighfall-Revival/blob/main/data/player_count_log.csv"
DISCORD_URL = "https://discord.gg/Jt58UeZf"

# ---------------------------------------------------------------------------
# Config (from config/settings.json)
# ---------------------------------------------------------------------------

def load_settings():
    try:
        with open(SETTINGS_FILE) as f:
            return json.load(f)
    except Exception as e:
        print(f"WARNING: Could not read settings.json ({e}), using defaults.")
        return {}

_settings = load_settings()

APP_ID          = _settings.get("app_id", 1911390)
PEAK_EVER       = _settings.get("peak_ever", 1512)
GOAL            = _settings.get("goal", 100)
ALERT_THRESHOLD = _settings.get("alert_threshold", 30)
MILESTONES      = _settings.get("milestones", [30, 50, 100])

# Credentials stay as environment variables / GitHub Secrets
GMAIL_USER         = os.getenv("GMAIL_USER", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")

# ---------------------------------------------------------------------------
# Subscriber list (from config/subscribers.csv)
# ---------------------------------------------------------------------------

def load_subscribers():
    """Return list of dicts for active subscribers."""
    if not os.path.exists(SUBSCRIBERS_FILE):
        print("WARNING: config/subscribers.csv not found — no alert emails will be sent.")
        return []
    with open(SUBSCRIBERS_FILE, newline="") as f:
        rows = list(csv.DictReader(f))
    active = [r for r in rows if r.get("active", "yes").strip().lower() == "yes"
              and r.get("email", "").strip()]
    return active

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
    notes = [r["note"] for r in rows if r["note"].startswith("MILESTONE")]
    reached = [int(n.split(":")[1].strip()) for n in notes if ":" in n]
    return max(reached) if reached else 0

# ---------------------------------------------------------------------------
# Email alert
# ---------------------------------------------------------------------------

def _render_template(count, milestone, trend_label, trend_color):
    progress = min(100, round(count / GOAL * 100))
    date_str = datetime.now(timezone.utc).strftime("%B %d, %Y")

    if count >= 30:
        accent_color = "#c9a227"
        mood_label   = "Alert"
        hero_title   = "There are enough players<br>online for a full lobby."
        cta_text     = "Jump on Discord"
    else:
        accent_color = "#586069"
        mood_label   = "Low Population"
        hero_title   = "Too quiet right now.<br>Help spread the word."
        cta_text     = "Join the Discord"

    try:
        with open(TEMPLATE_FILE, encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        return None
    for token, value in {
        "{{COUNT}}":        str(count),
        "{{MILESTONE}}":    str(milestone or count),
        "{{PROGRESS}}":     str(progress),
        "{{TREND_LABEL}}":  trend_label,
        "{{TREND_COLOR}}":  trend_color,
        "{{LOG_URL}}":      LOG_URL,
        "{{DISCORD_URL}}":  DISCORD_URL,
        "{{DATE}}":         date_str,
        "{{ACCENT_COLOR}}": accent_color,
        "{{MOOD_LABEL}}":   mood_label,
        "{{HERO_TITLE}}":   hero_title,
        "{{CTA_TEXT}}":     cta_text,
    }.items():
        html = html.replace(token, value)
    return html


def send_alerts(count, milestone=None, rows=None):
    """Send alert email to all active subscribers."""
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("ALERT: No Gmail credentials set — skipping emails.")
        return

    subscribers = load_subscribers()
    if not subscribers:
        print("ALERT: No active subscribers — skipping emails.")
        return

    if milestone == GOAL:
        subject = f"GOAL REACHED - Knightfall hit {count} players!"
    elif count >= 30:
        subject = f"Knightfall: {count} players online - lobby is filling!"
    else:
        subject = f"Knightfall: only {count} players online - help spread the word"

    # Trend from last 3 data points
    trend_label, trend_color = "FLAT", "#c9a227"
    if rows:
        recent = [int(r["player_count"]) for r in rows[-3:] if r["player_count"].isdigit()]
        if len(recent) >= 2:
            delta = recent[-1] - recent[0]
            if delta > 5:
                trend_label, trend_color = "UP", "#3fb950"
            elif delta < -5:
                trend_label, trend_color = "DOWN", "#f85149"

    html_body = _render_template(count, milestone, trend_label, trend_color)
    plain_body = (
        f"Knightfall: A Daring Journey — {count} players online\n"
        f"Goal: {GOAL} | Progress: {min(100, round(count / GOAL * 100))}%\n\n"
        f"View log: {LOG_URL}\n"
        f"Discord:  {DISCORD_URL}\n"
    )

    recipient_emails = [sub["email"].strip() for sub in subscribers]
    recipient_names  = [sub.get("name", sub["email"].strip()) for sub in subscribers]

    if html_body:
        msg = MIMEMultipart("alternative")
        msg.attach(MIMEText(plain_body, "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html", "utf-8"))
    else:
        msg = MIMEText(plain_body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"]    = GMAIL_USER
    msg["To"]      = ", ".join(recipient_emails)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, recipient_emails, msg.as_bytes())
            print(f"  Alert sent -> {', '.join(recipient_names)}")
    except Exception as e:
        print(f"ERROR sending alert emails: {e}")

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
            ts = datetime.strptime(r["timestamp"], "%Y-%m-%d %H:%M UTC").replace(tzinfo=timezone.utc)
            if ts >= cutoff and r["player_count"].isdigit():
                recent.append(int(r["player_count"]))
        except ValueError:
            pass

    subs = load_subscribers()
    print("=" * 42)
    print("  KNIGHTFALL PLAYER COUNT SUMMARY")
    print("=" * 42)
    print(f"  Latest logged:    {latest}")
    if recent:
        print(f"  7-day average:    {sum(recent) / len(recent):.1f}")
    print(f"  All-time peak:    {PEAK_EVER}")
    print(f"  Goal:             {GOAL}")
    print(f"  Progress:         {min(100, round(latest / GOAL * 100))}%")
    print(f"  Alert threshold:  {ALERT_THRESHOLD}")
    print(f"  Subscribers:      {len(subs)} active")
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

    if "--test-email" in sys.argv:
        print("Sending test email to all active subscribers...")
        count = fetch_player_count() or 11
        send_alerts(count, milestone=None, rows=[])
        return

    count = fetch_player_count()
    if count is None:
        append_log("ERROR")
        sys.exit(1)

    rows = load_log()
    prev_milestone = highest_milestone_reached(rows)

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

    if new_milestone:
        print(f"New milestone reached: {new_milestone} players!")
        send_alerts(count, milestone=new_milestone, rows=rows)
    elif count >= ALERT_THRESHOLD and prev_milestone == 0:
        send_alerts(count, rows=rows)


if __name__ == "__main__":
    main()

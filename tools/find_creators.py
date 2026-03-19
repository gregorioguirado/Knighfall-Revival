"""
Tool: find_creators.py
Purpose: Search YouTube for content creators who cover niche/indie/hidden-gem PC games
         and output a ranked target list for Knightfall creator outreach.
Output: .tmp/creator_targets.csv
"""

import os
import csv
import sys

# YouTube Data API v3 key — add to .env as YOUTUBE_API_KEY=your_key_here
# Free quota: 10,000 units/day. This script uses ~100 units per run.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
OUTPUT_FILE = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".tmp", "creator_targets.csv"))

# Search queries targeting the right audience
SEARCH_QUERIES = [
    "hidden gem PC game 2024",
    "underrated indie game you never heard of",
    "dying game worth playing",
    "Landfall games review",
    "free battle royale PC hidden gem",
    "free steam game you should play",
]

TARGET_MIN_SUBS = 10_000
TARGET_MAX_SUBS = 500_000


def search_youtube(query, api_key, max_results=10):
    """Search YouTube for videos matching query, return channel info."""
    try:
        import urllib.request
        import urllib.parse
        import json

        params = urllib.parse.urlencode({
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": max_results,
            "key": api_key,
            "relevanceLanguage": "en",
            "videoCategoryId": "20",  # Gaming category
        })
        url = f"https://www.googleapis.com/youtube/v3/search?{params}"
        with urllib.request.urlopen(url, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"  Search error for '{query}': {e}")
        return None


def get_channel_stats(channel_id, api_key):
    """Fetch subscriber count and other stats for a channel."""
    try:
        import urllib.request
        import urllib.parse
        import json

        params = urllib.parse.urlencode({
            "part": "statistics,snippet",
            "id": channel_id,
            "key": api_key,
        })
        url = f"https://www.googleapis.com/youtube/v3/channels?{params}"
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read())
            if data.get("items"):
                item = data["items"][0]
                stats = item.get("statistics", {})
                snippet = item.get("snippet", {})
                return {
                    "subscriber_count": int(stats.get("subscriberCount", 0)),
                    "video_count": int(stats.get("videoCount", 0)),
                    "description": snippet.get("description", "")[:200],
                    "country": snippet.get("country", ""),
                }
    except Exception as e:
        print(f"  Stats error for channel {channel_id}: {e}")
    return None


def run_with_api(api_key):
    """Full run using YouTube Data API."""
    print(f"Searching YouTube for creator targets...")
    seen_channels = {}

    for query in SEARCH_QUERIES:
        print(f"  Query: '{query}'")
        results = search_youtube(query, api_key)
        if not results:
            continue

        for item in results.get("items", []):
            channel_id = item["snippet"]["channelId"]
            if channel_id in seen_channels:
                seen_channels[channel_id]["match_count"] += 1
                continue

            channel_title = item["snippet"]["channelTitle"]
            stats = get_channel_stats(channel_id, api_key)
            if not stats:
                continue

            subs = stats["subscriber_count"]
            if subs < TARGET_MIN_SUBS or subs > TARGET_MAX_SUBS:
                continue  # Outside target range

            seen_channels[channel_id] = {
                "channel_id": channel_id,
                "channel_name": channel_title,
                "subscriber_count": subs,
                "video_count": stats["video_count"],
                "country": stats["country"],
                "channel_url": f"https://youtube.com/channel/{channel_id}",
                "match_count": 1,
                "contacted": "No",
                "contact_date": "",
                "reply": "",
                "notes": "",
            }

    # Sort by match count (appeared in multiple searches = better fit), then by subs
    targets = sorted(seen_channels.values(), key=lambda x: (-x["match_count"], -x["subscriber_count"]))

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    fieldnames = ["channel_name", "subscriber_count", "match_count", "channel_url",
                  "video_count", "country", "contacted", "contact_date", "reply", "notes"]
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for t in targets:
            writer.writerow({k: t.get(k, "") for k in fieldnames})

    print(f"\nFound {len(targets)} creator targets in range {TARGET_MIN_SUBS:,}–{TARGET_MAX_SUBS:,} subs.")
    print(f"Saved to: {OUTPUT_FILE}")
    print("\nTop 5 targets:")
    for t in targets[:5]:
        print(f"  {t['channel_name']} — {t['subscriber_count']:,} subs — {t['channel_url']}")
    print(f"\nOpen {OUTPUT_FILE} to see the full list and track outreach.")


def run_without_api():
    """Fallback: print manual search instructions if no API key."""
    print("=" * 50)
    print("  NO YOUTUBE_API_KEY FOUND IN .env")
    print("=" * 50)
    print()
    print("To use this tool automatically:")
    print("1. Go to https://console.cloud.google.com/")
    print("2. Create a project → Enable 'YouTube Data API v3'")
    print("3. Create an API key → copy it")
    print("4. Add to .env: YOUTUBE_API_KEY=your_key_here")
    print("5. Re-run this script")
    print()
    print("--- MANUAL ALTERNATIVE (no API key needed) ---")
    print()
    print("Search YouTube manually for these queries and note channels:")
    for q in SEARCH_QUERIES:
        print(f'  "{q}"')
    print()
    print("Target channels with 10k–500k subscribers that cover indie PC games.")
    print(f"Log them in: {OUTPUT_FILE}")
    print()
    print("CSV columns to use:")
    print("  channel_name, subscriber_count, channel_url, contacted, contact_date, reply, notes")

    # Create empty CSV for manual use
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "channel_name", "subscriber_count", "channel_url",
                "contacted", "contact_date", "reply", "notes"
            ])
            writer.writeheader()
        print(f"\nEmpty template created at: {OUTPUT_FILE}")


def main():
    if not YOUTUBE_API_KEY:
        run_without_api()
    else:
        run_with_api(YOUTUBE_API_KEY)


if __name__ == "__main__":
    main()

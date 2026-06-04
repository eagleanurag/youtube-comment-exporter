import csv
import re
import os
import sys
import argparse
import requests

# Load API key from .env file if running locally
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


# ──────────────────────────────────────────────────────────
#  URL PARSER
# ──────────────────────────────────────────────────────────

def extract_video_id(user_input: str) -> str | None:
    """
    Extracts a YouTube video ID from any input format.

    Supported:
      Plain ID            CDTcQDBT8KI
      Standard URL        https://www.youtube.com/watch?v=CDTcQDBT8KI
      With timestamp      https://youtu.be/CDTcQDBT8KI?t=42s
      With playlist       https://youtube.com/watch?v=ID&list=PL...
      YouTube Shorts      https://www.youtube.com/shorts/CDTcQDBT8KI
      YouTube Live        https://www.youtube.com/live/CDTcQDBT8KI
      Mobile URL          https://m.youtube.com/watch?v=CDTcQDBT8KI
      YouTube Music       https://music.youtube.com/watch?v=CDTcQDBT8KI
      Embed URL           https://www.youtube.com/embed/CDTcQDBT8KI
    """
    user_input = user_input.strip()

    # Plain 11-character video ID
    if re.match(r'^[A-Za-z0-9_-]{11}$', user_input):
        return user_input

    patterns = [
        r'[?&]v=([A-Za-z0-9_-]{11})',
        r'youtu\.be/([A-Za-z0-9_-]{11})',
        r'/shorts/([A-Za-z0-9_-]{11})',
        r'/live/([A-Za-z0-9_-]{11})',
        r'/embed/([A-Za-z0-9_-]{11})',
        r'/v/([A-Za-z0-9_-]{11})',
    ]

    for pattern in patterns:
        match = re.search(pattern, user_input)
        if match:
            return match.group(1)

    return None


# ──────────────────────────────────────────────────────────
#  INPUT HELPERS
# ──────────────────────────────────────────────────────────

def get_api_key() -> str:
    """
    Reads API key from environment variable YOUTUBE_API_KEY.

    Local:          Set in .env file
    GitHub Actions: Set in repository Secrets → Actions
    """
    api_key = os.getenv("YOUTUBE_API_KEY", "").strip()
    if not api_key:
        print("\n❌  API key not found.")
        print("    Local usage  : Add YOUTUBE_API_KEY=your_key to your .env file")
        print("    GitHub Actions: Add YOUTUBE_API_KEY to Settings → Secrets → Actions")
        print("\n    See README.md for full setup instructions.")
        sys.exit(1)
    return api_key


def get_video_id(url_arg: str | None) -> str:
    """
    Returns video ID from CLI argument or interactive prompt.
    """
    # Non-interactive mode (e.g. GitHub Actions)
    if url_arg:
        video_id = extract_video_id(url_arg)
        if not video_id:
            print(f"❌  Could not extract a video ID from: {url_arg}")
            sys.exit(1)
        print(f"  ✅  Video ID : {video_id}\n")
        return video_id

    # Interactive mode (local terminal)
    print("  Paste a YouTube URL or video ID:")
    print("  Works with: full URLs, short links, Shorts, Live, timestamps, playlists\n")
    while True:
        user_input = input("  > ").strip()
        if not user_input:
            print("  ⚠️   Please enter something.\n")
            continue
        video_id = extract_video_id(user_input)
        if video_id:
            print(f"\n  ✅  Video ID : {video_id}\n")
            return video_id
        print("  ❌  Could not find a video ID. Try again.\n")


def get_format(format_arg: str | None) -> bool:
    """
    Returns True for Excel, False for CSV.
    Uses CLI argument if provided, otherwise prompts.
    """
    if format_arg:
        return format_arg.lower() != "csv"

    print("  Export format:")
    print("    1. Excel (.xlsx)  — borders, bold header, auto-fit columns")
    print("    2. CSV   (.csv)   — plain text, opens in any app")
    choice = input("\n  Enter 1 or 2 (default: 1): ").strip() or "1"
    return choice != "2"


# ──────────────────────────────────────────────────────────
#  COMMENT FETCHING
# ──────────────────────────────────────────────────────────

def get_all_comments(video_id: str, api_key: str) -> list[dict]:
    """Fetches all top-level comments and replies via YouTube Data API v3."""
    all_rows   = []
    page_token = None
    page       = 1

    while True:
        print(f"  Fetching page {page}...", end="\r")

        params = {
            "part":       "snippet,replies",
            "videoId":    video_id,
            "maxResults": 100,
            "textFormat": "plainText",
            "key":        api_key,
        }
        if page_token:
            params["pageToken"] = page_token

        response = requests.get(
            "https://www.googleapis.com/youtube/v3/commentThreads",
            params=params,
            timeout=15,
        )
        data = response.json()

        if "error" in data:
            print(f"\n❌  API Error: {data['error']['message']}")
            sys.exit(1)

        for item in data.get("items", []):
            snippet    = item["snippet"]
            top        = snippet["topLevelComment"]["snippet"]
            comment_id = snippet["topLevelComment"]["id"]

            all_rows.append({
                "type":       "Main Comment",
                "parent_id":  "N/A",
                "comment_id": comment_id,
                "author":     top["authorDisplayName"],
                "likes":      top["likeCount"],
                "timestamp":  top["publishedAt"],
                "text":       top["textDisplay"].replace("\n", " "),
            })

            if snippet["totalReplyCount"] > 0:
                for reply in item.get("replies", {}).get("comments", []):
                    r = reply["snippet"]
                    all_rows.append({
                        "type":       "Reply",
                        "parent_id":  comment_id,
                        "comment_id": reply["id"],
                        "author":     r["authorDisplayName"],
                        "likes":      r["likeCount"],
                        "timestamp":  r["publishedAt"],
                        "text":       r["textDisplay"].replace("\n", " "),
                    })

        page_token = data.get("nextPageToken")
        if not page_token:
            break
        page += 1

    return all_rows


# ──────────────────────────────────────────────────────────
#  EXPORT FUNCTIONS
# ──────────────────────────────────────────────────────────

def export_csv(rows: list[dict], output_file: str):
    fieldnames = ["type", "parent_id", "comment_id", "author", "likes", "timestamp", "text"]
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def export_xlsx(rows: list[dict], output_file: str):
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, Border, Side

    wb = Workbook()
    ws = wb.active
    ws.title = "youtube_comments"

    headers    = ["type", "parent_id", "comment_id", "author", "likes", "timestamp", "text"]
    thin       = Side(border_style="thin", color="000000")
    borders    = Border(top=thin, bottom=thin, left=thin, right=thin)
    hdr_font   = Font(bold=True, size=14)
    hdr_align  = Alignment(horizontal="left", vertical="top")
    data_align = Alignment(horizontal="left", vertical="top")

    ws.append(headers)
    for cell in ws[1]:
        cell.font      = hdr_font
        cell.alignment = hdr_align
        cell.border    = borders

    for row in rows:
        ws.append([row["type"], row["parent_id"], row["comment_id"],
                   row["author"], row["likes"], row["timestamp"], row["text"]])

    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = data_align
            cell.border    = borders

    for col in ws.columns:
        max_len    = 0
        col_letter = col[0].column_letter
        for cell in col:
            if cell.value:
                max_len = max(max_len, len(str(cell.value)))
        ws.column_dimensions[col_letter].width = min(max_len + 4, 80)

    wb.save(output_file)


# ──────────────────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Export YouTube comments to Excel or CSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  python export_comments.py                              # interactive mode
  python export_comments.py --url https://youtu.be/ID   # non-interactive
  python export_comments.py --url ID --format csv       # CSV output
        """
    )
    parser.add_argument("--url",    help="YouTube video URL or video ID")
    parser.add_argument("--format", choices=["xlsx", "csv"], help="Export format (default: xlsx)")
    return parser.parse_args()


def main():
    args = parse_args()

    print("\n" + "=" * 55)
    print("  YouTube Comment Exporter")
    print("=" * 55 + "\n")

    api_key  = get_api_key()
    video_id = get_video_id(args.url)
    use_xlsx = get_format(args.format)

    print("-" * 55)
    print(f"  Video ID : {video_id}")
    print(f"  Format   : {'Excel (.xlsx)' if use_xlsx else 'CSV (.csv)'}")
    print("-" * 55)
    print("  Fetching comments...\n")

    rows = get_all_comments(video_id, api_key)

    script_dir  = os.path.dirname(os.path.abspath(__file__))
    ext         = "xlsx" if use_xlsx else "csv"
    output_file = os.path.join(script_dir, f"youtube_comments.{ext}")

    print(f"\n  Saving {len(rows)} rows as {ext.upper()}...")
    export_xlsx(rows, output_file) if use_xlsx else export_csv(rows, output_file)

    print("\n" + "=" * 55)
    print(f"  ✅  Done!  {len(rows)} comments + replies saved.")
    print(f"  📄  File : {output_file}")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()

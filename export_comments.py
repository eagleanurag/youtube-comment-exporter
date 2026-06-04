import csv
import requests
import os
import sys

# ─────────────────────────────────────────────
#  CONFIGURATION — edit these two lines only
# ─────────────────────────────────────────────
API_KEY  = "PASTE_YOUR_API_KEY_HERE"
VIDEO_ID = "CDTcQDBT8KI"
# ─────────────────────────────────────────────


def get_all_comments(video_id: str, api_key: str) -> list[dict]:
    """Fetches all top-level comments and their replies for a YouTube video."""
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


def export_csv(rows: list[dict], output_file: str):
    """Saves comments to a plain CSV file."""
    fieldnames = ["type", "parent_id", "comment_id", "author", "likes", "timestamp", "text"]
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def export_xlsx(rows: list[dict], output_file: str):
    """Saves comments to a formatted Excel file."""
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, Border, Side

    wb = Workbook()
    ws = wb.active
    ws.title = "youtube_comments"

    headers = ["type", "parent_id", "comment_id", "author", "likes", "timestamp", "text"]

    # --- Define styles ---
    thin_side   = Side(border_style="thin", color="000000")
    all_borders = Border(
        top=thin_side, bottom=thin_side,
        left=thin_side, right=thin_side
    )
    header_font      = Font(bold=True, size=14)
    header_alignment = Alignment(horizontal="left", vertical="top")
    data_alignment   = Alignment(horizontal="left", vertical="top")

    # --- Write header row ---
    ws.append(headers)
    for cell in ws[1]:
        cell.font      = header_font
        cell.alignment = header_alignment
        cell.border    = all_borders

    # --- Write data rows ---
    for row in rows:
        ws.append([
            row["type"], row["parent_id"], row["comment_id"],
            row["author"], row["likes"], row["timestamp"], row["text"]
        ])

    # --- Apply border + alignment to all data rows ---
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = data_alignment
            cell.border    = all_borders

    # --- Auto-fit column widths (based on content, capped at 80) ---
    for col in ws.columns:
        max_len    = 0
        col_letter = col[0].column_letter
        for cell in col:
            if cell.value:
                max_len = max(max_len, len(str(cell.value)))
        ws.column_dimensions[col_letter].width = min(max_len + 4, 80)

    wb.save(output_file)


def main():
    if API_KEY == "PASTE_YOUR_API_KEY_HERE":
        print("❌  Please set your API_KEY in the script before running.")
        sys.exit(1)

    # --- Ask export format ---
    print("\n  Export format:")
    print("    1. Excel (.xlsx)  — formatted with borders, bold header, auto-fit columns")
    print("    2. CSV   (.csv)   — plain text, universal compatibility")
    choice   = input("\n  Enter 1 or 2 (default: 1): ").strip() or "1"
    use_xlsx = choice != "2"

    print("\n" + "=" * 55)
    print("  YouTube Comment Exporter")
    print("=" * 55)
    print(f"  Video ID : {VIDEO_ID}")
    print(f"  API Key  : {'*' * (len(API_KEY) - 4)}{API_KEY[-4:]}")
    print(f"  Format   : {'Excel (.xlsx)' if use_xlsx else 'CSV (.csv)'}")
    print("-" * 55)
    print("  Fetching comments...\n")

    rows = get_all_comments(VIDEO_ID, API_KEY)

    script_dir  = os.path.dirname(os.path.abspath(__file__))
    ext         = "xlsx" if use_xlsx else "csv"
    output_file = os.path.join(script_dir, f"youtube_comments.{ext}")

    print(f"\n  Saving {len(rows)} rows as {ext.upper()}...")

    if use_xlsx:
        export_xlsx(rows, output_file)
    else:
        export_csv(rows, output_file)

    print("\n" + "=" * 55)
    print(f"  ✅  Done! {len(rows)} comments + replies saved.")
    print(f"  📄  File : {output_file}")
    print("=" * 55)


if __name__ == "__main__":
    main()

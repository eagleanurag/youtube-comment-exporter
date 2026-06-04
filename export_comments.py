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
    """
    Fetches all top-level comments and their replies for a YouTube video.

    Args:
        video_id: The YouTube video ID (the part after ?v= in the URL).
        api_key:  A valid YouTube Data API v3 key.

    Returns:
        A list of dicts, each representing one comment or reply.
    """
    all_rows  = []
    page_token = None
    page      = 1

    while True:
        print(f"  Fetching page {page}...", end="\r")

        params = {
            "part":        "snippet,replies",
            "videoId":     video_id,
            "maxResults":  100,
            "textFormat":  "plainText",
            "key":         api_key,
        }
        if page_token:
            params["pageToken"] = page_token

        response = requests.get(
            "https://www.googleapis.com/youtube/v3/commentThreads",
            params=params,
            timeout=15,
        )
        data = response.json()

        # Handle API errors gracefully
        if "error" in data:
            print(f"\n❌  API Error: {data['error']['message']}")
            sys.exit(1)

        for item in data.get("items", []):
            snippet    = item["snippet"]
            top        = snippet["topLevelComment"]["snippet"]
            comment_id = snippet["topLevelComment"]["id"]

            # Add the top-level comment
            all_rows.append({
                "type":       "Main Comment",
                "parent_id":  "N/A",
                "comment_id": comment_id,
                "author":     top["authorDisplayName"],
                "likes":      top["likeCount"],
                "timestamp":  top["publishedAt"],
                "text":       top["textDisplay"].replace("\n", " "),
            })

            # Add all replies (if any exist)
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


def main():
    if API_KEY == "PASTE_YOUR_API_KEY_HERE":
        print("❌  Please set your API_KEY in the script before running.")
        sys.exit(1)

    print("=" * 50)
    print("  YouTube Comment Exporter")
    print("=" * 50)
    print(f"  Video ID : {VIDEO_ID}")
    print(f"  API Key  : {'*' * (len(API_KEY) - 4)}{API_KEY[-4:]}")
    print("-" * 50)
    print("  Fetching comments...\n")

    rows = get_all_comments(VIDEO_ID, API_KEY)

    # Save to the same folder as this script
    script_dir  = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "youtube_comments.csv")

    fieldnames = ["type", "parent_id", "comment_id", "author", "likes", "timestamp", "text"]
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("\n" + "=" * 50)
    print(f"  ✅  Done!  {len(rows)} comments + replies saved.")
    print(f"  📄  File  : {output_file}")
    print("=" * 50)


if __name__ == "__main__":
    main()

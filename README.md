<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=32&pause=1000&color=FF0000&center=true&vCenter=true&random=false&width=700&height=70&lines=YouTube+Comment+Exporter+%F0%9F%93%A5;Any+URL+%E2%86%92+Full+Comment+Export;Run+Locally+or+via+GitHub+Actions;API+Key+Always+Safe+%F0%9F%94%92" alt="Typing SVG" />

<br/>

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![YouTube API](https://img.shields.io/badge/YouTube-Data+API+v3-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://developers.google.com/youtube/v3)
[![GitHub Actions](https://img.shields.io/badge/GitHub-Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](../../actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Excel](https://img.shields.io/badge/Output-Excel%20%2F%20CSV-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white)]()

<br/>

> 🚀 **Paste any YouTube URL — get every comment and reply exported to a formatted Excel or CSV file.**  
> Run locally or trigger from GitHub Actions. Your API key is always hidden and secure.

<br/>

[Features](#-features) • [How It Works](#-how-it-works) • [Local Setup](#-local-setup) • [GitHub Actions Setup](#-github-actions-setup) • [URL Formats](#-supported-url-formats) • [Output](#-output-format)

</div>

---

## ✨ Features

<table>
<tr>
<td>

- 📥 **Fetches ALL comments** — no artificial limits
- 💬 **Includes every reply** to every top-level comment
- 🔗 **Handles any YouTube URL** — paste and go
- 🔒 **Fully secure** — API key is never in code or repo

</td>
<td>

- ☁️ **Run from GitHub** — no local Python needed
- 📊 **Auto-formatted Excel** — borders, bold header, auto-fit
- 💾 **Auto-saves** output as a downloadable artifact
- 🛠️ **Works both ways** — interactive CLI or GitHub Actions

</td>
</tr>
</table>

---

## 🔐 How It Works — Security Model

Your API key is **never stored in the code or repository**.

| Where you run it | Where the key lives |
|-----------------|---------------------|
| Local machine | `.env` file — on your PC only, blocked by `.gitignore` |
| GitHub Actions | GitHub Secrets — encrypted, only visible to workflows |

```
Your PC                          GitHub
┌─────────────────┐              ┌──────────────────────────┐
│  .env file      │              │  Settings → Secrets      │
│  (never pushed) │              │  YOUTUBE_API_KEY = ****  │
│                 │              │  (encrypted, hidden)     │
│  export_        │              │                          │
│  comments.py ───┼─reads key───▶│  GitHub Actions Workflow │
│                 │              │  (runs script securely)  │
└─────────────────┘              └──────────────────────────┘
```

---

## 📁 Project Structure

```
youtube-comment-exporter/
├── 📄 export_comments.py            ← Main script
├── 📋 requirements.txt              ← Dependencies
├── 🔑 .env.example                  ← API key template (copy → .env)
├── 🚫 .gitignore                    ← Keeps .env and outputs out of Git
├── 📝 README.md
├── ⚖️  LICENSE
├── 🤝 CONTRIBUTING.md
└── 📁 .github/
    ├── workflows/
    │   └── export_comments.yml      ← GitHub Actions workflow
    └── ISSUE_TEMPLATE/
        ├── bug_report.md
        └── feature_request.md
```

---

## 💻 Local Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/eagleanurag/youtube-comment-exporter.git
cd youtube-comment-exporter
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Get a YouTube Data API v3 key

<details>
<summary><b>Click to expand step-by-step</b></summary>
<br/>

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click **"New Project"** → name it → **Create**
3. Sidebar → **APIs & Services** → **Library**
4. Search **"YouTube Data API v3"** → Click → **Enable**
5. Sidebar → **Credentials** → **+ Create Credentials** → **API Key**
6. Copy the key shown

> ✅ Free quota: 10,000 units/day — enough for most videos.

</details>

### 4️⃣ Create your `.env` file

```bash
# Windows
copy .env.example .env

# Mac / Linux
cp .env.example .env
```

Open `.env` in Notepad and paste your key:

```env
YOUTUBE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

> ✅ `.env` is in `.gitignore` — it will **never** be pushed to GitHub.

### 5️⃣ Run it

```bash
python export_comments.py
```

```
=======================================================
  YouTube Comment Exporter
=======================================================

  Paste a YouTube URL or video ID:
  Works with: full URLs, short links, Shorts, Live, timestamps, playlists

  > https://youtu.be/CDTcQDBT8KI?t=42s

  ✅  Video ID : CDTcQDBT8KI

  Export format:
    1. Excel (.xlsx)  — borders, bold header, auto-fit columns
    2. CSV   (.csv)   — plain text, opens in any app

  Enter 1 or 2 (default: 1):

  ✅  Done!  250 comments + replies saved.
  📄  File : C:\Users\you\Desktop\youtube-comment-exporter\youtube_comments.xlsx
```

---

## ☁️ GitHub Actions Setup

Run the export directly from your GitHub repo — **no local Python needed**.  
Your API key is stored as a GitHub Secret — encrypted and never visible to anyone.

### Step 1 — Add your API key as a GitHub Secret

1. Go to your repository on GitHub
2. Click **Settings** (top menu)
3. Left sidebar → **Secrets and variables** → **Actions**
4. Click **"New repository secret"**
5. Name: `YOUTUBE_API_KEY`
6. Value: your API key
7. Click **"Add secret"**

> ✅ GitHub encrypts this secret. It shows as `***` everywhere — even in workflow logs.

### Step 2 — Run the workflow

1. Go to your repo → click **Actions** tab
2. Left sidebar → click **"Export YouTube Comments"**
3. Click **"Run workflow"** (top right)
4. Fill in the inputs:

```
YouTube video URL or video ID:   https://youtu.be/CDTcQDBT8KI
Export format:                   xlsx
```

5. Click the green **"Run workflow"** button

### Step 3 — Download your file

1. Click the workflow run once it appears
2. Wait for it to complete (green ✅)
3. Scroll to **Artifacts** at the bottom
4. Click **"youtube-comments-1"** to download your file

> ✅ Files are kept for **7 days** then automatically deleted.

---

## 🔗 Supported URL Formats

| Format | Example |
|--------|---------|
| Standard URL | `https://www.youtube.com/watch?v=CDTcQDBT8KI` |
| With timestamp | `https://www.youtube.com/watch?v=CDTcQDBT8KI&t=42s` |
| With playlist | `https://youtube.com/watch?v=CDTcQDBT8KI&list=PL...` |
| Short URL | `https://youtu.be/CDTcQDBT8KI` |
| Short + timestamp | `https://youtu.be/CDTcQDBT8KI?t=42` |
| YouTube Shorts | `https://www.youtube.com/shorts/CDTcQDBT8KI` |
| YouTube Live | `https://www.youtube.com/live/CDTcQDBT8KI` |
| Mobile URL | `https://m.youtube.com/watch?v=CDTcQDBT8KI` |
| YouTube Music | `https://music.youtube.com/watch?v=CDTcQDBT8KI` |
| Embed URL | `https://www.youtube.com/embed/CDTcQDBT8KI` |
| Plain video ID | `CDTcQDBT8KI` |

---

## 📊 Output Format

### Excel (.xlsx) — Auto-formatted

| Formatting | Applied automatically |
|------------|----------------------|
| **Header row** | Bold, font size 14, left + top aligned |
| **All cells** | Thin border on all 4 sides |
| **All rows** | Left aligned, top aligned |
| **Column widths** | Auto-fitted to content |

### Columns (both Excel and CSV)

| Column | Description | Example |
|--------|-------------|---------|
| `type` | Comment type | `Main Comment` / `Reply` |
| `parent_id` | Parent comment ID | `Ugx8s...` / `N/A` |
| `comment_id` | Unique YouTube comment ID | `Ugx8sKd3...` |
| `author` | Display name of commenter | `@JohnDoe` |
| `likes` | Number of likes | `42` |
| `timestamp` | Date & time posted (ISO 8601) | `2024-01-15T08:30:00.000Z` |
| `text` | Full comment text | `Great video!` |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| ![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white) | Core language |
| ![YouTube](https://img.shields.io/badge/-YouTube%20API%20v3-FF0000?style=flat&logo=youtube&logoColor=white) | Comment data source |
| ![GitHub Actions](https://img.shields.io/badge/-GitHub%20Actions-2088FF?style=flat&logo=githubactions&logoColor=white) | Cloud execution |
| `requests` | HTTP calls to the API |
| `openpyxl` | Excel file creation and formatting |
| `python-dotenv` | Secure API key loading from `.env` |

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature/my-feature`
3. Commit: `git commit -m "Add my feature"`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

---

## 📄 License

Licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

<div align="center">

**If this project helped you, please consider giving it a ⭐**

<br/>

Made with ❤️ by [Anurag](https://github.com/eagleanurag)

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=14&pause=1000&color=888888&center=true&vCenter=true&width=400&lines=Thanks+for+visiting!+%F0%9F%91%8B" alt="footer" />

</div>

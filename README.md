<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=32&pause=1000&color=FF0000&center=true&vCenter=true&random=false&width=700&height=70&lines=YouTube+Comment+Exporter+%F0%9F%93%A5;Export+All+Comments+%26+Replies;Excel+%2B+CSV+Output+in+Seconds;Powered+by+YouTube+Data+API+v3" alt="Typing SVG" />

<br/>

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![YouTube API](https://img.shields.io/badge/YouTube-Data+API+v3-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://developers.google.com/youtube/v3)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Excel](https://img.shields.io/badge/Output-Excel%20%2F%20CSV-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge)](CONTRIBUTING.md)

<br/>

> 🚀 **Export every comment & reply from any YouTube video into a formatted Excel or CSV file — in seconds.**

<br/>

[Features](#-features) • [Quick Start](#-quick-start) • [Output Format](#-output-format) • [API Setup](#-get-your-api-key) • [Contributing](#-contributing)

</div>

---

## ✨ Features

<table>
<tr>
<td>

- 📥 **Fetches ALL comments** — no artificial limits
- 💬 **Includes every reply** to every top-level comment
- 📊 **Excel export** with auto-formatting applied automatically
- ⚡ **Fast** — uses YouTube's official Data API v3

</td>
<td>

- 🔒 **Safe & reliable** — no scraping bans or hacks
- 💾 **Auto-saves** to the same folder as the script
- 🔁 **Handles pagination** — works on videos with thousands of comments
- 🛠️ **Choice of format** — Excel (.xlsx) or CSV at runtime

</td>
</tr>
</table>

---

## 📁 Project Structure

```
youtube-comment-exporter/
├── 📄 export_comments.py        ← Main script
├── 📋 requirements.txt          ← Dependencies
├── 📝 README.md                 ← You are here
├── ⚖️  LICENSE                  ← MIT License
├── 🤝 CONTRIBUTING.md           ← Contribution guide
└── 📁 .github/
    └── ISSUE_TEMPLATE/
        ├── bug_report.md
        └── feature_request.md
```

---

## 🚀 Quick Start

### 1️⃣ Clone the repository

```bash
git clone https://github.com/eagleanurag/youtube-comment-exporter.git
cd youtube-comment-exporter
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Get your API key → [see instructions below](#-get-your-api-key)

### 4️⃣ Set your API key and Video ID

Open `export_comments.py` and update these two lines:

```python
API_KEY  = "YOUR_API_KEY_HERE"
VIDEO_ID = "CDTcQDBT8KI"    # ← the part after ?v= in the YouTube URL
```

### 5️⃣ Run it

```bash
python export_comments.py
```

You'll be asked to choose your export format:

```
  Export format:
    1. Excel (.xlsx)  — formatted with borders, bold header, auto-fit columns
    2. CSV   (.csv)   — plain text, universal compatibility

  Enter 1 or 2 (default: 1):
```

```
  ✅  Done! 250 comments + replies saved.
  📄  File : C:\Users\you\Desktop\youtube-comment-exporter\youtube_comments.xlsx
```

---

## 🔑 Get Your API Key

<details>
<summary><b>Click to expand step-by-step instructions</b></summary>

<br/>

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click **"New Project"** → give it a name → **Create**
3. In the sidebar go to **APIs & Services** → **Library**
4. Search for **"YouTube Data API v3"** → Click it → **Enable**
5. Go to **APIs & Services** → **Credentials**
6. Click **"+ Create Credentials"** → **API Key**
7. Copy the key shown — paste it into the script

> ✅ The free quota (10,000 units/day) is more than enough for most videos.

</details>

---

## 📊 Output Format

### Excel (.xlsx) — Auto-formatted

When you choose Excel, the file is automatically formatted:

| Formatting | Applied |
|------------|---------|
| **Header row** | Bold, font size 14, left + top aligned |
| **All cells** | Thin border on all 4 sides |
| **All rows** | Left aligned, top aligned |
| **Column widths** | Auto-fitted to content |

### Columns (both formats)

| Column | Description | Example |
|--------|-------------|---------|
| `type` | Comment type | `Main Comment` / `Reply` |
| `parent_id` | Parent comment ID (replies only) | `Ugx8s...` / `N/A` |
| `comment_id` | Unique YouTube comment ID | `Ugx8sKd3...` |
| `author` | Display name of commenter | `@JohnDoe` |
| `likes` | Number of likes on the comment | `42` |
| `timestamp` | Date & time posted (ISO 8601) | `2024-01-15T08:30:00.000Z` |
| `text` | Full comment text | `Great video!` |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| ![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white) | Core language |
| ![YouTube](https://img.shields.io/badge/-YouTube%20API%20v3-FF0000?style=flat&logo=youtube&logoColor=white) | Comment data source |
| `requests` | HTTP calls to the API |
| `openpyxl` | Excel file creation and formatting |
| `csv` | CSV file writing |
| `os` | Cross-platform file paths |

---

## ⚙️ Configuration Options

You can tweak these variables at the top of `export_comments.py`:

| Variable | Default | Description |
|----------|---------|-------------|
| `API_KEY` | `""` | Your YouTube Data API v3 key |
| `VIDEO_ID` | `""` | YouTube video ID (from the URL) |

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repo
2. Create a branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -m "Add my feature"`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

<div align="center">

**If this project helped you, please consider giving it a ⭐ — it means a lot!**

<br/>

Made with ❤️ by [Anurag](https://github.com/eagleanurag)

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=14&pause=1000&color=888888&center=true&vCenter=true&width=400&lines=Thanks+for+visiting!+%F0%9F%91%8B" alt="footer" />

</div>

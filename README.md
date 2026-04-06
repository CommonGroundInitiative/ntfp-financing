# NTFP Public Financing — Ready Reckoner

A searchable, filterable database of Government of India financing schemes for Non-Timber Forest Product (NTFP) value chains. Built as an open-source project by [Dakshin Foundation](https://dakshin.org).

**Live app:** `https://CommonGroundInitiative.github.io/ntfp-financing/`

---

## What's in here

| File/Folder | Purpose |
|---|---|
| `index.html` | The web app (React, runs in the browser) |
| `data/schemes.xlsx` | Source data — **edit this to update schemes** |
| `data/schemes.json` | Auto-generated from Excel; also serves as a static API |
| `scripts/excel_to_json.py` | Converts Excel → JSON |
| `scripts/seed_supabase.py` | Loads JSON into Supabase |
| `.github/workflows/sync_data.yml` | Auto-runs when Excel is updated |
| `supabase_schema.sql` | Paste into Supabase SQL Editor to set up the database |

---

## Using the app

The app has six tabs:

- **Browse & Filter** — search and filter all 30+ schemes by ministry, recipient type, activity, financing type, and socio-economic preference
- **Eligibility Matcher** — answer a few questions to see which schemes you qualify for
- **Compare** — select up to four schemes side-by-side
- **Contribute** — suggest a new scheme or an update to an existing one (goes into a pending queue for admin review)
- **Admin** — approve or reject pending contributions (requires Supabase login)
- **For Developers** — API documentation and iframe embed code

---

## Public API

### Static JSON (no auth required)

```
GET https://raw.githubusercontent.com/CommonGroundInitiative/ntfp-financing/main/data/schemes.json
```

This is the full dataset as a JSON array. Updated automatically when the Excel file changes.

**Example — fetch in JavaScript:**
```js
const res  = await fetch("https://raw.githubusercontent.com/CommonGroundInitiative/ntfp-financing/main/data/schemes.json");
const data = await res.json();
console.log(data);
```

**Example — fetch in Python:**
```python
import requests
schemes = requests.get(
    "https://raw.githubusercontent.com/CommonGroundInitiative/ntfp-financing/main/data/schemes.json"
).json()
```

---

### Live REST API (Supabase — requires anon key in header)

Base URL: `https://<project>.supabase.co/rest/v1/`

**Required header:**
```
apikey: <your-anon-public-key>
```

#### Get all active schemes
```bash
curl "https://<project>.supabase.co/rest/v1/schemes?status=eq.active" \
  -H "apikey: <anon-key>"
```

#### Filter by socio-economic preference
```bash
curl "https://<project>.supabase.co/rest/v1/schemes?status=eq.active&socio_economic_preference=eq.ST" \
  -H "apikey: <anon-key>"
```

#### Get schemes with all their activities (nested)
```bash
curl "https://<project>.supabase.co/rest/v1/schemes?status=eq.active&select=*,scheme_activities(*)" \
  -H "apikey: <anon-key>"
```

#### Example — fetch in JavaScript
```js
const ANON = "<your-anon-key>";
const URL  = "https://<project>.supabase.co/rest/v1/schemes?status=eq.active&select=*,scheme_activities(*)";
const res  = await fetch(URL, { headers: { apikey: ANON } });
const data = await res.json();
```

#### Example — fetch in Python
```python
import requests
ANON = "<your-anon-key>"
URL  = "https://<project>.supabase.co/rest/v1/schemes?status=eq.active"
schemes = requests.get(URL, headers={"apikey": ANON}).json()
```

---

## Embed the app

Paste this into any webpage:

```html
<iframe
  src="https://CommonGroundInitiative.github.io/ntfp-financing/"
  width="100%"
  height="800"
  style="border:none;border-radius:8px">
</iframe>
```

---

## Updating the data

1. Download `data/schemes.xlsx` from this repo
2. Make your changes
3. Upload the updated file (same path: `data/schemes.xlsx`) via GitHub's browser UI
4. The GitHub Action runs automatically: Excel → JSON → Supabase
5. The live app reflects the changes within ~2 minutes

---

## First-time setup

See the steps below if you're setting this up from scratch.

### 1. Create a Supabase project

1. Go to [supabase.com](https://supabase.com) → New project
2. In the **SQL Editor**, paste and run the contents of `supabase_schema.sql`
3. Copy your **Project URL**, **anon/public key**, and **service key** from Project Settings → API

### 2. Configure GitHub Secrets

In your GitHub repo → Settings → Secrets and variables → Actions → New repository secret:

| Secret name | Value |
|---|---|
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_SERVICE_KEY` | Your service key (not the anon key) |

### 3. Configure the web app

Open `index.html` and fill in the config block near the top:

```js
const SUPABASE_URL  = "https://yourproject.supabase.co";
const SUPABASE_ANON = "your-anon-public-key";
const GITHUB_USER   = "your-github-username";
const GITHUB_REPO   = "ntfp-schemes";
```

### 4. Seed the database

Run this once from your Mac terminal (Python 3 required):

```bash
SUPABASE_URL=https://yourproject.supabase.co \
SUPABASE_SERVICE_KEY=your-service-key \
python3 scripts/seed_supabase.py
```

### 5. Enable GitHub Pages

In your repo → Settings → Pages → Source: `main` branch, `/ (root)` → Save.

Your app will be live at `https://CommonGroundInitiative.github.io/ntfp-financing/`.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to suggest a new scheme or an update to an existing one.

---

## License

Data is sourced from publicly available Government of India scheme documents.
Code is released under the [MIT License](LICENSE).

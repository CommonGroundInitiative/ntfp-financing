# Contributing to NTFP Public Financing — Ready Reckoner

Thank you for helping keep this resource up to date. There are two ways to suggest changes.

---

## Option 1 — Web form (easiest)

Use the **Contribute** tab in the app:

1. Open the app at `https://CommonGroundInitiative.github.io/ntfp-financing/`
2. Click the **Contribute** tab
3. Choose **"Add a new scheme"** or **"Suggest an update to an existing scheme"**
4. Fill in as many fields as you can — partial information is welcome
5. Click **Submit**

Your submission goes into a pending queue. The maintainers will review it and either approve it (making it visible to everyone) or reach out if they need more information.

---

## Option 2 — GitHub Issue

If you have a GitHub account, you can open an issue:

1. Click [New Issue](../../issues/new) in this repo
2. Use the title format: `[New scheme] Scheme Name` or `[Update] Scheme Name`
3. Include:
   - **Scheme name**
   - **Ministry** responsible
   - **Fund recipient** (e.g., State government, FPO, Individual)
   - **End recipient type** (e.g., Tribal household, SHG, Cooperative)
   - **Value chain activity** (e.g., Collection, Processing, Marketing)
   - **Financing type** (e.g., Grant, Loan, Subsidy)
   - **Financing notes** (amount, conditions, limits)
   - **Link** to the official scheme document or website
   - **Socio-economic preference** (ST only / SC & ST / Open to All)
   - **Central or State scheme** — if State, which state?

---

## What happens next

- Submissions via the web form appear in the admin panel as **pending**
- A maintainer reviews, can edit if needed, then approves or rejects
- Approved schemes appear in the app immediately
- GitHub Issues are reviewed periodically and added to the Excel file

---

## Updating the Excel directly (for maintainers)

If you have write access to this repo:

1. Download `data/schemes.xlsx`
2. Add or edit rows following the existing column structure
3. Upload the updated file to `data/schemes.xlsx` via GitHub (drag and drop)
4. The GitHub Action runs automatically and syncs everything within ~2 minutes

Column order in the Excel:
| Column | Field |
|---|---|
| A | Scheme No. |
| B | Scheme Name |
| C | Ministry |
| D | Fund Recipient |
| E | End Recipient Type |
| F | Value Chain Activity |
| G | Financing Type |
| H | Socio-Economic Preference |
| I | State / Central |
| J | Financing Notes |
| K | Link |

Each row is one activity. A scheme with multiple activities has multiple rows (same scheme name in column B).

---

## Code contributions

Pull requests are welcome for bug fixes and UI improvements. Please open an issue first for larger changes so we can discuss the approach.

# Lab 2: The Efficiency Gap and Gill v. Whitford

In this lab you will analyze Wisconsin Assembly election data and compute the **efficiency gap** — the metric at the center of the *Gill v. Whitford* gerrymandering case.

## Getting Started with GitHub Codespaces

The easiest way to complete this lab is using GitHub Codespaces, which runs everything in your browser.

### Step 1: Open in Codespaces

Click the green **Code** button above, then select **Open with Codespaces** > **New codespace**.

### Step 2: Wait for Setup

The codespace will:
1. Build the development environment (1-2 minutes)
2. Install required packages
3. **Automatically open Marimo** in a new browser tab

If Marimo doesn't open automatically, you can run:
```bash
uv run marimo edit notebooks/lab02/lab02.py --host 0.0.0.0 --port 2718
```

### Step 3: Complete the Notebook

In the Marimo interface, work through the exercises on computing and interpreting the efficiency gap.

### Step 4: Submit Your Work

Once you've completed the notebook, commit and push your changes:

**Option A: Using the terminal**
```bash
git add notebooks/lab02/lab02.py
git commit -m "Complete Lab 2"
git push
```

**Option B: Using VS Code**
1. Click the Source Control icon in the left sidebar
2. Stage your changes (+ button)
3. Enter a commit message
4. Click "Commit" then "Sync Changes"

## Running Locally (Alternative)

If you prefer to run locally instead of using Codespaces:

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
2. Clone this repository
3. Install dependencies:
   ```bash
   uv sync
   ```
4. Open the notebook:
   ```bash
   uv run marimo edit notebooks/lab02/lab02.py
   ```

## Troubleshooting

**Marimo tab didn't open?**
- Check the "Ports" tab in VS Code and click on port 2718
- Or run the marimo command manually (see Step 2)

**Package errors?**
- Try running `uv sync` in the terminal

**Can't push changes?**
- Make sure you accepted the GitHub Classroom assignment first
- Check that you're signed into GitHub in the codespace

## Need Help?

If you encounter issues, post on the course discussion board or come to office hours.

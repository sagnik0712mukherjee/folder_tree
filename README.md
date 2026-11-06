# 📁 Folder Tree Viewer (Mac)

A tiny, free Mac app. Double-click it and it shows everything in its own folder as a neat, collapsible tree. No typing, no choosing, no setup.

## For users

1. Unzip the download to get **Folder Tree Viewer**.
2. Drag the app (using Finder) into the folder you want to look at.
3. Double-click it. A window opens showing that folder as a collapsible tree. Click any folder to open or close it.

Move the app into a different folder and it shows *that* folder instead. There is nothing to type or choose.

Handy buttons in the window:
- **Refresh** – update the view after folders change.
- **Show / hide files** – include or leave out individual files.
- **Expand all** – opens every folder, all the way down to the lowest level. Click **Show / hide files** as well to see the files inside them.
- **Collapse all** – closes everything back to the top folder.
- **Search box** – type part of a folder name to find it.

The app only *reads* folder names. It never changes, moves, or deletes anything, and it needs no internet.

### First-time security steps (once only)

This app is free and not "code-signed" by Apple, so the Mac blocks it the first time.

1. Double-click the app and click **Done** on the "could not verify" message (not Move to Bin).
2. Open **Apple menu → System Settings → Privacy & Security**.
3. Scroll to **Security**, click **Open Anyway** next to the app's name, and confirm with your password or Touch ID. (The button stays for about an hour; if it's gone, double-click the app again.)

On older Macs, right-click the app and choose **Open** instead.

Other messages:
- **"One quick step":** in Finder, drag the app into the folder you want to view and double-click it there.
- **Access to Desktop, Documents or Downloads:** click **Allow**.

Requirements: a Mac with Apple Silicon (M1 or newer).

## Downloads

Go to the **Actions** tab of this repository, open the latest successful run, and download `Folder-Tree-Viewer-Mac`. Unzip it once to get `Folder-Tree-Viewer-Mac.zip`, which holds the app.

## For the person maintaining this

Project layout:

```
foldertree.py                  Scans folders and builds the HTML tree page
foldertree_app.py              The double-click window (shows the folder the app is in)
.github/workflows/build.yml    Builds the Mac app for free on GitHub
```

**Build with GitHub:** open the **Actions** tab → *Build Folder Tree Viewer* → **Run workflow**. Free Mac machines are sometimes busy; if the job fails with "not acquired by Runner", use **Re-run failed jobs** or build on your own Mac below.

**Build on your own Mac:**

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pyinstaller --noconsole --windowed --exclude-module tkinter --name "Folder Tree Viewer" foldertree_app.py
ditto -c -k --keepParent "dist/Folder Tree Viewer.app" Folder-Tree-Viewer-Mac.zip
```

The app is created in `dist/`, and the zip is the file to send to others.

**Run from source (needs Python 3.10+):**

```
pip install pywebview
python3 foldertree_app.py          # shows the folder this script is in
```

**Quick command-line mode (no window):**

```
python3 foldertree.py "/Users/you/Music"          # folders only
python3 foldertree.py "/Users/you/Music" --files  # include files
```

**Notes:**
- Very large folders are capped at 30,000 items so the app stays responsive.
- Folders the Mac won't let the app open are shown with a 🔒.
- Mac `.app` bundles are shown as a single item instead of their inner folders.
- A log is written to `folder_tree_viewer_log.txt` in the system temp folder to help diagnose problems.
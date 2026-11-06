# 📁 Folder Tree Viewer

A tiny, free app for Windows and Mac. Double-click it and it shows everything in its own folder as a neat, collapsible tree. No typing, no choosing, no setup.

## For users

1. Put the app inside the folder you want to look at.
2. Double-click it.
3. A window opens showing everything inside that folder as a neat, collapsible tree. Click any folder to open or close it.

Move the app into a different folder and it shows *that* folder instead. There is nothing to type or choose.

Handy buttons in the window:
- **Refresh** – update the view after folders change.
- **Show / hide files** – include or leave out individual files.
- **Expand all / Collapse all** – open or close every folder at once.
- **Search box** – type part of a folder name to find it.

The app only *reads* folder names. It never changes, moves, or deletes anything, and it needs no internet.

### First-time warnings (normal)

This app is free and not "code-signed", so your computer will ask once if you're sure.

- **Windows:** if you see *"Windows protected your PC"*, click **More info**, then **Run anyway**.
- **Mac:** right-click (or Control-click) the app, choose **Open**, then click **Open** again.
- **Mac, right after downloading:** if the window says "One quick step", drag the app (in Finder) into the folder you want to view and double-click it there. This is needed only once.
- **Mac, privacy question:** if the app sits in Desktop, Documents or Downloads, the Mac asks whether the app may access that folder. Click **Allow**.

## Downloads

Go to the **Actions** tab of this repository, open the latest successful run, and download:

- `Folder-Tree-Viewer-Windows` → contains `Folder Tree Viewer.exe`
- `Folder-Tree-Viewer-Mac` → contains a zip; unzip it to get `Folder Tree Viewer.app`

Requirements: Windows 10/11, or a Mac with Apple Silicon (M1 or newer).

## For the person maintaining this

Project layout:

```
foldertree.py                  Scans folders and builds the HTML tree page
foldertree_app.py              The double-click window (shows the folder the app is in)
.github/workflows/build.yml    Builds the Windows .exe and Mac .app for free
```

**Sharing with others:** see `SHARING.md`; forward `HOW_TO_USE.txt` to users.

**Build the apps:** open the **Actions** tab → *Build Folder Tree Viewer* → **Run workflow**. Builds take about 5 minutes.

**Run from source (needs Python 3.10+):**

```
pip install pywebview
python foldertree_app.py          # shows the folder this script is in
```

**Quick command-line mode (no window):**

```
python foldertree.py "C:\path\to\folder"          # folders only
python foldertree.py "C:\path\to\folder" --files  # include files
```

**Notes:**
- Very large folders are capped at 30,000 items so the app stays responsive.
- Folders the computer won't let the app open are shown with a 🔒.
- To support older Intel Macs, add an Intel macOS job to `build.yml`.

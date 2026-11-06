# How to share Folder Tree Viewer with stakeholders

## 1. Get the final app files
1. On GitHub, open the **Actions** tab and click the latest run with a green tick.
2. At the bottom, under **Artifacts**, download `Folder-Tree-Viewer-Windows` and `Folder-Tree-Viewer-Mac`.
3. Unzip each download once. You now have `Folder Tree Viewer.exe` (Windows) and `Folder-Tree-Viewer-Mac.zip` (Mac).

## 2. Make a permanent download link (recommended)
Actions downloads expire after 90 days and need a GitHub login, so publish a Release instead.
1. On the repo's main page, click **Releases → Create a new release**.
2. Click **Choose a tag**, type `v1.0`, then click **Create new tag**.
3. Title it `Folder Tree Viewer v1.0`.
4. Drag in `Folder Tree Viewer.exe` and `Folder-Tree-Viewer-Mac.zip`.
5. Click **Publish release**. Anyone with the link can download without a GitHub account (the repo must be Public).

## 3. Send it
Pick one:
- **Release link** – copy the Release page URL and send it by WhatsApp or email. Tell Windows people to click the `.exe` and Mac people to click the `.zip`.
- **Google Drive / OneDrive** – upload both files and share a link.
- **Pen drive or AirDrop** – fine for people sitting next to you.

Notes:
- Gmail and Outlook often block `.exe` attachments. Use a link, not an attachment.
- Mac users: send the `.zip`, never a loose `.app`.

## 4. Send the one-page guide
Forward `HOW_TO_USE.txt` (or paste its text into the message) so people expect the first-time warning screens.

## 5. Help the first person through it
- **Windows:** "More info" then "Run anyway" (once).
- **Mac:** right-click the app, **Open**, **Open** (once). If it says "One quick step", drag the app into the target folder in Finder and open it there.

## 6. When you change the app
Edit the file on GitHub, wait for the green build, then publish a new Release (`v1.1`, `v1.2`...) with the new files and send the new link.

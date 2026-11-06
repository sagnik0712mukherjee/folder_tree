"""
Folder Tree Viewer
------------------
Give it a folder path, get a beautiful, collapsible folder tree.

Windows / Mac / Linux:  double-click or run  `python foldertree.py`
Command line:           python foldertree.py "C:\\Users\\Sagnik\\Music"
Only standard Python is needed (no installs).
"""

import os
import sys
import html
import tempfile
import webbrowser
from datetime import datetime

MAX_NODES = 30000  # safety cap so huge drives don't freeze the app


# ---------- 1. Scan the folders ----------
def scan(path, include_files, state):
    """Return a dict: {name, folders:[...], files:[...]} for the given path."""
    node = {"name": os.path.basename(path.rstrip("\\/")) or path, "folders": [], "files": []}
    try:
        entries = sorted(os.scandir(path), key=lambda e: e.name.lower())
    except (PermissionError, FileNotFoundError, OSError):
        node["locked"] = True
        return node

    for entry in entries:
        if state["count"] >= MAX_NODES:
            state["truncated"] = True
            break
        try:
            if entry.is_dir(follow_symlinks=False):
                state["count"] += 1
                state["folders"] += 1
                if entry.name.lower().endswith(".app"):
                    # Mac apps are folders inside; show them as one item.
                    node["folders"].append({"name": entry.name, "folders": [], "files": []})
                else:
                    node["folders"].append(scan(entry.path, include_files, state))
            elif include_files:
                state["count"] += 1
                state["files"] += 1
                node["files"].append(entry.name)
        except OSError:
            continue
    return node


def count_sub(node):
    return len(node["folders"]) + sum(count_sub(f) for f in node["folders"])


# ---------- 2. Turn the tree into pretty HTML ----------
def render(node, is_root=False):
    name = html.escape(node["name"])
    locked = " 🔒" if node.get("locked") else ""
    files_html = "".join(
        f'<div class="file">📄 {html.escape(f)}</div>' for f in node["files"]
    )
    if not node["folders"] and not node["files"]:
        return f'<div class="leaf">📁 <span class="n">{name}</span>{locked}</div>'

    subs = count_sub(node)
    badge = f'<span class="badge">{subs}</span>' if subs else ""
    children = "".join(render(f) for f in node["folders"]) + files_html
    open_attr = " open" if is_root else ""
    return (
        f'<details{open_attr}><summary>📂 <span class="n">{name}</span>{locked} {badge}</summary>'
        f'<div class="kids">{children}</div></details>'
    )


PAGE = """<!doctype html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Folder Tree</title>
<style>
  :root { --bg:#0f1220; --card:#171b2e; --text:#e8eaf6; --muted:#8b91b3; --accent:#7c9cff; --line:#2a3050; }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--text);
         font-family:-apple-system,"Segoe UI",Roboto,sans-serif; padding:24px 16px; }
  .wrap { max-width:900px; margin:0 auto; }
  h1 { font-size:22px; margin:0 0 4px; }
  .path { color:var(--accent); word-break:break-all; font-size:14px; }
  .meta { color:var(--muted); font-size:13px; margin:6px 0 16px; }
  .bar { display:flex; gap:8px; flex-wrap:wrap; margin-bottom:16px; }
  input, button { background:var(--card); color:var(--text); border:1px solid var(--line);
         border-radius:10px; padding:10px 14px; font-size:14px; }
  input { flex:1; min-width:180px; }
  button { cursor:pointer; } button:hover { border-color:var(--accent); }
  .tree { background:var(--card); border:1px solid var(--line); border-radius:16px; padding:16px 12px; }
  details, .leaf, .file { margin:2px 0; }
  summary { cursor:pointer; padding:5px 8px; border-radius:8px; list-style:none; }
  summary::-webkit-details-marker { display:none; }
  summary:hover, .leaf:hover { background:#20254080; }
  .leaf { padding:5px 8px; border-radius:8px; }
  .kids { margin-left:14px; padding-left:14px; border-left:1px dashed var(--line); }
  .file { padding:3px 8px; color:var(--muted); font-size:13px; }
  .badge { background:#2a3050; color:var(--accent); border-radius:999px;
           font-size:11px; padding:2px 8px; margin-left:6px; }
  mark { background:#ffd86b; color:#000; border-radius:3px; }
  .warn { color:#ffb86b; font-size:13px; margin-bottom:12px; }
</style></head>
<body><div class="wrap">
  <h1>📁 Folder Tree</h1>
  <div class="path">__PATH__</div>
  <div class="meta">__META__</div>
  __WARN__
  <div class="bar">
    <input id="q" placeholder="Search folder names…" oninput="find(this.value)">
    <button onclick="setAll(true)">Expand all</button>
    <button onclick="setAll(false)">Collapse all</button>
  </div>
  <div class="tree" id="tree">__TREE__</div>
</div>
<script>
  function setAll(open){ document.querySelectorAll('details').forEach(d=>d.open=open); }
  function find(t){
    t=t.trim().toLowerCase();
    document.querySelectorAll('.n').forEach(s=>{ s.innerHTML=s.textContent; });
    if(!t) return;
    document.querySelectorAll('.n').forEach(s=>{
      const x=s.textContent, i=x.toLowerCase().indexOf(t);
      if(i>=0){
        s.innerHTML=x.slice(0,i)+'<mark>'+x.slice(i,i+t.length)+'</mark>'+x.slice(i+t.length);
        let p=s.parentElement; while(p){ if(p.tagName==='DETAILS') p.open=true; p=p.parentElement; }
      }
    });
  }
</script></body></html>"""


def build_html(path, include_files):
    state = {"count": 0, "folders": 0, "files": 0, "truncated": False}
    tree = scan(path, include_files, state)
    meta = f"{state['folders']} folders"
    if include_files:
        meta += f" · {state['files']} files"
    meta += f" · created {datetime.now():%d %b %Y, %H:%M}"
    warn = ""
    if state["truncated"]:
        warn = f'<div class="warn">⚠ Very large folder — showing the first {MAX_NODES:,} items only.</div>'
    return (
        PAGE.replace("__PATH__", html.escape(path))
        .replace("__META__", meta)
        .replace("__WARN__", warn)
        .replace("__TREE__", render(tree, is_root=True))
    )


def make_and_open(path, include_files=False):
    path = os.path.abspath(os.path.expanduser(path.strip().strip('"')))
    if not os.path.isdir(path):
        raise ValueError(f"This folder was not found:\n{path}")
    out = os.path.join(tempfile.gettempdir(), "folder_tree.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(build_html(path, include_files))
    webbrowser.open("file://" + out.replace("\\", "/"))
    return out


# ---------- 3. Simple window for non-technical users ----------
def run_gui():
    import tkinter as tk
    from tkinter import filedialog, messagebox

    root = tk.Tk()
    root.title("Folder Tree Viewer")
    root.geometry("560x230")
    root.configure(bg="#0f1220")

    tk.Label(root, text="📁 Folder Tree Viewer", font=("Segoe UI", 16, "bold"),
             bg="#0f1220", fg="#e8eaf6").pack(pady=(18, 4))
    tk.Label(root, text="Paste a folder path, or click Browse.",
             bg="#0f1220", fg="#8b91b3").pack()

    row = tk.Frame(root, bg="#0f1220")
    row.pack(pady=12, padx=20, fill="x")
    path_var = tk.StringVar()
    tk.Entry(row, textvariable=path_var, font=("Segoe UI", 11)).pack(side="left", fill="x", expand=True, ipady=4)

    def browse():
        p = filedialog.askdirectory()
        if p:
            path_var.set(p)

    tk.Button(row, text="Browse…", command=browse).pack(side="left", padx=(8, 0))

    files_var = tk.BooleanVar(value=False)
    tk.Checkbutton(root, text="Also show files", variable=files_var, bg="#0f1220", fg="#e8eaf6",
                   selectcolor="#171b2e", activebackground="#0f1220",
                   activeforeground="#e8eaf6").pack()

    def go():
        try:
            make_and_open(path_var.get(), files_var.get())
        except Exception as e:
            messagebox.showerror("Oops", str(e))

    tk.Button(root, text="Show Tree", command=go, bg="#7c9cff", fg="black",
              font=("Segoe UI", 11, "bold"), padx=18, pady=4).pack(pady=12)
    root.mainloop()


# ---------- 4. Start-up ----------
if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    with_files = "--files" in sys.argv
    if args:                       # command line: python foldertree.py "path"
        print("Created:", make_and_open(args[0], with_files))
    else:
        try:
            run_gui()              # normal double-click use
        except Exception:          # no window support (e.g. phone shells)
            p = input("Enter folder path: ")
            print("Created:", make_and_open(p, with_files))

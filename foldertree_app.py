"""
Folder Tree Viewer - double-click app
-------------------------------------
Double-click it and the window shows the folder tree of the folder the app is
sitting in. No questions asked. Move the app to another folder and it will show
that folder instead.

Needs foldertree.py in the same folder when run from source (it draws the tree).
"""

import os
import sys
import html

import foldertree as ft

LOADING = """<!doctype html><html><head><meta charset="utf-8">
<style>body{margin:0;height:100vh;display:flex;align-items:center;justify-content:center;
background:#0f1220;color:#8b91b3;font-family:-apple-system,"Segoe UI",Roboto,sans-serif;font-size:18px}</style>
</head><body>Reading folder&hellip;</body></html>"""

MESSAGE = """<!doctype html><html><head><meta charset="utf-8">
<style>body{margin:0;height:100vh;display:flex;align-items:center;justify-content:center;
background:#0f1220;color:#e8eaf6;font-family:-apple-system,"Segoe UI",Roboto,sans-serif;text-align:center}
div{max-width:520px;padding:24px;line-height:1.5} h1{font-size:24px} p{color:#b9bedb}</style>
</head><body><div><h1>__TITLE__</h1><p>__TEXT__</p></div></body></html>"""

TOOLBAR_EXTRA = (
    '<button onclick="pywebview.api.refresh()">&#128260; Refresh</button>'
    '<button onclick="pywebview.api.toggle_files()">&#128196; Show / hide files</button>'
)


def app_folder():
    """The folder this app lives in (works for .exe, Mac .app, or plain script)."""
    if getattr(sys, "frozen", False):
        exe = os.path.realpath(sys.executable)
        if sys.platform == "darwin":
            parts = exe.split(os.sep)
            for i, part in enumerate(parts):
                if part.lower().endswith(".app"):
                    return os.sep.join(parts[:i]) or os.sep
        return os.path.dirname(exe)
    return os.path.dirname(os.path.abspath(__file__))


def is_translocated():
    """Mac runs freshly downloaded apps from a hidden temporary place."""
    return sys.platform == "darwin" and "AppTranslocation" in os.path.realpath(sys.executable)


def message_page(title, text):
    return MESSAGE.replace("__TITLE__", html.escape(title)).replace("__TEXT__", html.escape(text))


def make_page(path, include_files):
    """Tree page for `path`, with the extra in-app buttons added."""
    page = ft.build_html(path, include_files)
    marker = '<button onclick="setAll(true)">'
    return page.replace(marker, TOOLBAR_EXTRA + marker, 1)


class Api:
    """Functions the page can call (the buttons)."""

    def __init__(self):
        self.window = None
        self.include_files = False

    def show(self):
        if is_translocated():
            self.window.load_html(message_page(
                "One quick step",
                "Please drag this app, using Finder, into the folder you want to look at, "
                "then double-click it there. (Mac needs this once after a download.)"))
            return
        path = app_folder()
        try:
            self.window.set_title("Folder Tree Viewer - " + (os.path.basename(path) or path))
            self.window.load_html(make_page(path, self.include_files))
        except Exception as e:
            self.window.load_html(message_page("Could not read this folder", str(e)))

    def refresh(self):
        self.window.load_html(LOADING)
        self.show()

    def toggle_files(self):
        self.include_files = not self.include_files
        self.refresh()


def main():
    import webview

    api = Api()
    api.window = webview.create_window(
        "Folder Tree Viewer", html=LOADING, js_api=api, width=1000, height=760
    )
    webview.start(api.show)  # runs as soon as the window is up


if __name__ == "__main__":
    main()

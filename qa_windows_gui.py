"""Hosted Windows Browser -2 Tk GUI evidence, without live network/browser actions."""
from __future__ import annotations

import argparse
import json
import tempfile
import time
from pathlib import Path
from unittest.mock import patch
import tkinter as tk
from tkinter import ttk
from PIL import ImageGrab

from browser_runner import BrowserRunner
from desktop_app import BrowserAutomationDesktop
from guided_config import make_screenshot_workflow


def capture(root, folder, name):
    root.deiconify()
    root.lift()
    root.focus_force()
    root.update()
    time.sleep(.3)
    root.update()
    x, y = root.winfo_rootx(), root.winfo_rooty()
    w, h = root.winfo_width(), root.winfo_height()
    if w < 880 or h < 640:
        raise AssertionError(f"Window too small: {w}x{h}")
    image = ImageGrab.grab(bbox=(x, y, x+w, y+h))
    path = folder / name
    image.save(path)
    if path.stat().st_size < 4500:
        raise AssertionError("Screenshot missing or empty")
    return {"filename": path.name, "dimensions": [w, h], "bytes": path.stat().st_size}


def run(output: Path):
    output.mkdir(parents=True, exist_ok=True)
    results = []
    with tempfile.TemporaryDirectory(prefix="browser-v2-qa-") as t:
        root_folder = Path(t)
        root = tk.Tk()
        try:
            app = BrowserAutomationDesktop(root)
            root.geometry("1024x768+35+35")
            root.update()
            if app.notebook.index("end") != 3:
                raise AssertionError("Expected three editable navigation tabs")
            app.lang = "ja"
            app._build()
            root.update()
            results.append({"check": "ja_guide", **capture(root, output, "browser-v2-ja-1024x768.png")})

            # Only synthetic local root and read-only dry-run. Never launch Chromium.
            with patch("desktop_app.filedialog.askdirectory", return_value=str(root_folder)):
                app._choose_guide_root()
            assert app.guide_root.get() == str(root_folder)
            config = make_screenshot_workflow(
                root_dir=str(root_folder), url="https://example.com/", filename="qa.png")
            with patch("browser_runner.sync_playwright",
                       side_effect=AssertionError("A preview must not launch a browser")):
                BrowserRunner(config, dry_run=True).run()
            if (root_folder / "qa.png").exists():
                raise AssertionError("Offline preview modified the filesystem")
            results.append({"check": "preview_no_network_no_file", "passed": True})

            app.notebook.select(app.step_tab)
            root.update()
            results.append({"check": "ja_step_builder", **capture(root, output, "browser-v2-ja-steps-1024x768.png")})
            app.notebook.select(app.advanced_tab)
            root.update()
            results.append({"check": "ja_review_tab", **capture(root, output, "browser-v2-ja-review-1024x768.png")})

            app.lang = "en"
            app._build()
            root.geometry("1280x720+35+35")
            root.update()
            if "Start here" not in app.notebook.tab(0, "text"):
                raise AssertionError("English tab localization did not apply")
            if app._live_running:
                raise AssertionError("GUI smoke must never start browser execution")
            results.append({"check": "en_guide", **capture(root, output, "browser-v2-en-1280x720.png")})
            app.notebook.select(app.advanced_tab)
            root.update()
            results.append({"check": "en_review", **capture(root, output, "browser-v2-en-review-1280x720.png")})
        finally:
            root.destroy()
    report = {"product": "Browser Automation Runner -2",
              "scope": "CI Tk UI and offline configuration only",
              "live_site_access": False, "real_browser_run": False,
              "human_windows_acceptance": False, "msix_installed": False,
              "checks": results}
    (output / "gui_qa_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("BROWSER-V2-GUI-QA PASS: "+json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("gui-review-evidence"))
    args = parser.parse_args()
    run(args.output)

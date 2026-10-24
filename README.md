# Browser Automation Runner -2

Consumer-first Windows browser automation. This is separate from the developer/regular Browser Automation Runner.

## What is implemented
- Select a local save folder (not hand-typing it), HTTPS target and screenshot filename.
- Guided setup, optional click/fill/download step builder, explicit Dry Run followed by separate real-browser approval.
- Restricted allow-listed hosts and local output collision protections.
- Japanese / English UI labels.

No claim is made that any Web page can be automatically understood, logged into or successfully automated. No AI recorder. Live website execution requires manual QA and user authorization.

## Provenance and status
- Ported exact source from `shihuiarenjinba-png/browser-automation-runner` SHA `5834e34afc3a061256d426a53c245bef64d9e643`, on 2026-10-24.
- Initial -2 working branch: `codex/consumer-v2-initial-20261024`. No main/release changes.
- QA build produces an **unsigned EXE with Chromium assets**, NOT a Store MSIX.
- New -2 Identity, Publisher, Store ID, PFN and Version are **UNKNOWN/HOLD**.
- Third-party licences/NOTICE/Chromium rights, Windows runtime GUI, JP/EN, login-related errors, 1024×768/1280×720 all still require review.
- No live Google/website login and no MS Store submission or publication in this stage.

Run local tests: `python -m unittest discover -s tests -v`. For Windows QA EXE: `./build_windows.ps1`.

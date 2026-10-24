# Browser -2 QA / Microsoft Store Gate

**QA only — NOT READY FOR STORE.**

Current source port: `b042a46bc8fd440fc4692aa78d456bd790623d3e`.
Source review: `shihuiarenjinba-png/browser-automation-runner` at `5834e34afc3a061256d426a53c245bef64d9e643`.

## Required Windows review
- English/Japanese UI, Save/Open, start/stop, Dry Run preflight with no network, explicit live confirmation.
- Chromium startup at exact artifact SHA; screenshot in local folder; no overwrite of existing output, allow-list enforcement, invalid URL and login expiry.
- 1024x768, 1280x720 and high-DPI UI.
- Chromium / Playwright / codecs third-party license and NOTICE audit. Do not certify if unverified.

## Store safety
- Current QA workflow builds Windows EXE (UNSIGNED) only.
- New product Microsoft Store ID, Package Identity, Publisher, PFN, Version are UNKNOWN/HOLD. Never port older MSIX manifest or Store ID.
- No Store submission or publication without explicit user authorization.
- Do not promise generic AI recorded automation or arbitrary website support.

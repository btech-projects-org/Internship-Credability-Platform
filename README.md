Project Overview
This workspace contains the frontend pages and backend services for the Internship Credibility system. The backend runs in a separate Python virtual environment to ensure stable ML dependencies.

Backend Environment
- Interpreter: C:\venv_icm\Scripts\python.exe
- Installed: tensorflow-cpu 2.20.0, transformers, datasets, scikit-learn, numpy, pandas, kaggle, huggingface-hub

Quick Checks
- Verify imports: run C:\venv_icm\Scripts\python.exe backend/scripts/check_imports.py
- TensorFlow note: oneDNN optimizations are enabled; set TF_ENABLE_ONEDNN_OPTS=0 for deterministic ops.

Browser Video Note
- The HTML uses the `playsinline` attribute for inline video playback on iOS Safari. Firefox does not support `playsinline`, which can trigger an informational warning. Keep `playsinline` as-is; it is required for iOS and does not break Firefox.

Tips
- If IDE still shows missing-import diagnostics, reload the window after switching the interpreter.
- For backend scripts, prefer the short-path venv to avoid Windows long-path issues.

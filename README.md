# Internship Credibility Check

Automated system to verify internship offer authenticity and assess credibility using AI/ML.

## Quick Start (Users)

### Windows 10/11

1. **Download** `CredibilityCheck.exe`
2. **Double-click** it
3. **Use** the web interface that opens automatically

No installation. No configuration. Just run and go.

---

## For Developers

### Build the Executable

```bash
build.bat
```

Generates `dist/CredibilityCheck.exe` (standalone, shareable, zero-setup).

### Develop Locally

```bash
pip install -r backend/requirements.txt
cd backend
python app.py
```

Then open: http://localhost:5000

---

## Features

✅ **Parse Internship Details** — Extract company, position, salary, duration from raw text
✅ **Credibility Analysis** — AI-powered scoring (0-100%)
✅ **Red Flags** — Detect fraud indicators (suspicious salary, fake domain, etc.)
✅ **Company Verification** — Auto-lookup official website via Google Search
✅ **Sentiment Analysis** — Analyze job description for red flags
✅ **URL Analysis** — Check domain age, registrar, patterns
✅ **Full Documentation** — See `documentation/project_overview.html`

---

## System Requirements

### To Run the Application
- Windows 10/11 (64-bit)
- ~500 MB disk space
- No Python, no pip, no setup

### To Build the Executable
- Windows 10/11 (64-bit)
- Python 3.12+
- ~3 GB for dependencies
- 5-10 minutes build time

---

## Architecture

| Component | Tech |
|-----------|------|
| **Backend** | Flask (Python) |
| **Frontend** | HTML, CSS, JavaScript |
| **ML Models** | scikit-learn, PyTorch |
| **Packaging** | PyInstaller (single .exe) |

---

## Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)** — Complete setup and distribution guide
- **[documentation/project_overview.html](documentation/project_overview.html)** — Full architecture & file reference

---

## API (For Integration)

Backend runs on `http://localhost:5000`

```bash
# Parse internship details
curl -X POST http://localhost:5000/api/parse_internship_info \
  -H "Content-Type: application/json" \
  -d '{"text": "internship offer text here"}'

# Get credibility analysis
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"company": "Google", "salary": 20000, ...}'
```

---

## FAQ

**Q: Is it safe to run?**  
A: Yes, it's your own code. Open-source and auditable at repository root.

**Q: What data is collected?**  
A: None. Everything runs locally on your machine. No cloud requests except for optional company website lookup.

**Q: Can I modify it?**  
A: Yes! Full source code included. Edit files, rebuild with `build.bat`.

**Q: Does it work offline?**  
A: Yes, except for the company website lookup feature (requires internet for Google Search API).

**Q: Why is the .exe so large?**  
A: It bundles Python, all ML libraries, and the entire application. This enables true zero-setup.

---

## License

[Your License Here]

---

## Support

For issues, questions, or feature requests:
- Check [DEPLOYMENT.md](DEPLOYMENT.md) troubleshooting section
- Review [documentation/project_overview.html](documentation/project_overview.html)
- [Your contact/support info here]

---

**Download → Double-click → Done.**

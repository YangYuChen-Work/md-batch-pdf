#!/usr/bin/env python3
"""Markdown → PDF batch converter.

Scans Input/ recursively for .md files, converts them to PDF
with GitHub-like styling, saves to Output/ mirroring the directory structure.

Uses the system's built-in browser (Edge/Chrome) for PDF rendering —
no extra downloads needed.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

import markdown
from pygments.formatters import HtmlFormatter


# ── Browser detection ────────────────────────────────────────────────────────

def _find_browser() -> str | None:
    """Find a Chromium-based browser for headless PDF printing."""
    if sys.platform == "win32":
        candidates = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
    elif sys.platform == "darwin":
        candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
        ]
    else:
        candidates = [
            "google-chrome", "google-chrome-stable",
            "chromium-browser", "chromium",
            "microsoft-edge",
        ]

    for path in candidates:
        if Path(path).exists():
            return path
    return None


BROWSER = _find_browser()


# ── GitHub-like CSS ──────────────────────────────────────────────────────────

CSS = """
body {
  font-family: "Segoe UI", "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Arial, sans-serif;
  font-size: 15px;
  line-height: 1.7;
  color: #24292f;
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 20px;
}

h1 { font-size: 2em; border-bottom: 1px solid #d8dee4; padding-bottom: .3em; margin-top: 32px; }
h2 { font-size: 1.5em; border-bottom: 1px solid #d8dee4; padding-bottom: .3em; margin-top: 28px; }
h3 { font-size: 1.25em; margin-top: 24px; }
h4 { font-size: 1em; margin-top: 24px; }

p { margin: 0 0 16px; }
a { color: #0969da; text-decoration: none; }
strong { font-weight: 600; }

code {
  font-family: "Cascadia Code", "Fira Code", Consolas, "Courier New", monospace;
  background: #f6f8fa;
  padding: .2em .4em;
  border-radius: 4px;
  font-size: 85%;
}

pre {
  background: #f6f8fa;
  border-radius: 6px;
  padding: 16px;
  overflow-x: auto;
  line-height: 1.45;
}
pre code {
  background: none;
  padding: 0;
  font-size: 100%;
  border-radius: 0;
}

table {
  border-collapse: collapse;
  width: 100%;
  margin: 0 0 16px;
}
th, td {
  border: 1px solid #d8dee4;
  padding: 8px 13px;
  text-align: left;
}
th { background: #f6f8fa; font-weight: 600; }
tr:nth-child(even) td { background: #f6f8fa; }

blockquote {
  border-left: 4px solid #d0d7de;
  color: #656d76;
  padding: 0 1em;
  margin: 0 0 16px;
}

ul, ol { padding-left: 2em; margin-bottom: 16px; }
li + li { margin-top: .25em; }

img { max-width: 100%; }
hr { border: 0; border-top: 1px solid #d8dee4; margin: 24px 0; }

.codehilite { background: #f6f8fa; border-radius: 6px; padding: 16px; overflow-x: auto; }
.codehilite pre { background: none; padding: 0; margin: 0; }
"""

# Append pygments syntax-highlighting color rules (GitHub-like light theme)
CSS += HtmlFormatter(style="friendly").get_style_defs(".codehilite")



# ── Conversion logic ─────────────────────────────────────────────────────────

def find_md_files(input_dir: Path) -> list[Path]:
    return sorted(input_dir.rglob("*.md"))


def md_to_html(md_path: Path) -> str:
    text = md_path.read_text(encoding="utf-8")
    return markdown.markdown(
        text,
        extensions=[
            "fenced_code",
            "tables",
            "codehilite",
            "toc",
            "nl2br",
        ],
        extension_configs={
            "codehilite": {
                "guess_lang": False,
                "css_class": "codehilite",
            },
        },
    )


def build_full_html(body: str, title: str) -> str:
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>{CSS}</style>
</head>
<body>
{body}
</body>
</html>"""


def convert_file(md_path: Path, input_dir: Path, output_dir: Path) -> str | None:
    """Convert a single .md to .pdf. Returns error string or None on success."""
    rel_path = md_path.relative_to(input_dir)
    pdf_path = output_dir / rel_path.with_suffix(".pdf")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    body = md_to_html(md_path)
    html = build_full_html(body, md_path.stem)

    with tempfile.NamedTemporaryFile(
        suffix=".html", mode="w", encoding="utf-8", delete=False
    ) as f:
        f.write(html)
        tmp_html = f.name

    try:
        # Edge headless mode requires --disable-gpu on some systems
        subprocess.run(
            [
                BROWSER,
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                "--no-pdf-header-footer",
                f"--print-to-pdf={pdf_path}",
                f"file:///{tmp_html}",
            ],
            check=True,
            timeout=30,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return None
    except subprocess.TimeoutExpired:
        return "Timeout (30s)"
    except subprocess.CalledProcessError as e:
        return f"Browser error (code {e.returncode})"
    except FileNotFoundError:
        return "Browser not found"
    finally:
        Path(tmp_html).unlink(missing_ok=True)


def main() -> int:
    root = Path(__file__).resolve().parent
    input_dir = root / "Input"
    output_dir = root / "Output"

    if BROWSER is None:
        print("Error: No supported browser found for PDF rendering.")
        print("Please install Google Chrome or Microsoft Edge.")
        return 1

    print(f"Browser: {BROWSER}")

    if not input_dir.exists():
        print(f"Error: Input folder not found: {input_dir}")
        return 1

    md_files = find_md_files(input_dir)

    if not md_files:
        print("No .md files found. Please put files into the Input/ folder.")
        return 0

    print(f"Found {len(md_files)} Markdown file(s)\n")

    ok, fail = 0, 0
    for i, md_path in enumerate(md_files, 1):
        rel = md_path.relative_to(input_dir)
        print(f"[{i}/{len(md_files)}] {rel}  ", end="", flush=True)
        err = convert_file(md_path, input_dir, output_dir)
        if err is None:
            print("OK")
            ok += 1
        else:
            print(f"X {err}")
            fail += 1

    print(f"\n--- Done ---")
    print(f"  Success: {ok}  Failed: {fail}")
    print(f"  Output:  {output_dir}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

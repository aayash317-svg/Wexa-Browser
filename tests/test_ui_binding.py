"""
UI and Frontend Integration Verification.
Ensures index.html, styles.css, and app.js are in sync with strict monochrome design tokens
and all DOM elements referenced in JavaScript exist in HTML.
"""

import re
from pathlib import Path
import pytest

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
HTML_PATH = FRONTEND_DIR / "index.html"
CSS_PATH = FRONTEND_DIR / "styles.css"
JS_PATH = FRONTEND_DIR / "app.js"


def test_frontend_files_exist():
    assert HTML_PATH.exists()
    assert CSS_PATH.exists()
    assert JS_PATH.exists()


def test_strict_black_and_white_color_tokens():
    css_content = CSS_PATH.read_text(encoding="utf-8")
    
    # Assert monochrome palette tokens exist
    assert "--bg-pure-black: #000000;" in css_content
    assert "--text-white: #ffffff;" in css_content or "--text-white: #FFFFFF;" in css_content
    
    # Ensure no forbidden color hexes in :root tokens
    forbidden_colors = [
        "#1E6FFF",  # Old blue
        "#38BDF8",  # Old cyan
        "#10B981",  # Old green
        "#F59E0B",  # Old yellow
        "#FF5F56",  # Mac red
        "#27C93F",  # Mac green
        "#FFBD2E",  # Mac yellow
    ]
    for color in forbidden_colors:
        assert color.lower() not in css_content.lower(), f"Forbidden color {color} found in styles.css"


def test_html_and_js_id_bindings():
    html_content = HTML_PATH.read_text(encoding="utf-8")
    js_content = JS_PATH.read_text(encoding="utf-8")
    
    html_ids = set(re.findall(r'id=["\']([a-zA-Z0-9_-]+)["\']', html_content))
    js_ids = set(re.findall(r'getElementById\(["\']([a-zA-Z0-9_-]+)["\']', js_content))
    
    missing = js_ids - html_ids
    assert not missing, f"JavaScript references elements not found in HTML: {missing}"


def test_features_present_in_ui():
    html_content = HTML_PATH.read_text(encoding="utf-8")
    js_content = JS_PATH.read_text(encoding="utf-8")
    
    # 1. Search button
    assert "navGoBtn" in html_content
    assert "nav-search-btn" in html_content
    
    # 2. Upload URL / Custom Problem modal
    assert "uploadModal" in html_content
    assert "btnUploadModal" in html_content
    
    # 3. Presets modal
    assert "presetsModal" in html_content
    assert "btnPresetsMenu" in html_content
    
    # 4. Animated Page Loading bar
    assert "pageLoadingBar" in html_content
    assert "page-loading-bar" in html_content
    
    # 5. Dataset Inspector modal
    assert "datasetsModal" in html_content
    assert "datasetsTableBody" in html_content

